"""File profile for de-identifying dicom files"""
import collections
import datetime
import gzip
import logging
import os
import re
import sys
import tempfile
import types

import pydicom
import pydicom.datadict
import pydicom.tag
from pydicom.filewriter import writers
from pydicom.charset import text_VRs
from pydicom.data import get_testdata_files
import six
from fs.osfs import OSFS
from flywheel_metadata.file.dicom.fixer import fw_pydicom_config

from ..util import date_delta, is_dicom, dict_paths, walk_dicom_wild_sequence
from .file_profile import FileProfile
from .deid_field import DeIdField

log = logging.getLogger(__name__)

DICOM_TAG_HEX_RE = re.compile(r"^(0x)?[0-9a-fA-F]{8}$")
DICOM_TAG_TUPLE_RE = re.compile(r"\(\s*([0-9a-fA-F]{4})\s*,\s*([0-9a-fA-F]{4})\s*\)")
# match data element in sequence
DICOM_NESTED_RE = re.compile(
    r"^(?:([0-9A-Fa-f]{8}|[\w]+)\.([\d]?[*]?)\.)+([0-9A-Fa-f]{8}|[\w]+)$"
)


class DicomTagStr(str):
    """Subclass of string that has a _dicom_tag and _is_sequence attribute"""

    def __new__(cls, value, *_args, **_kwargs):
        return super(DicomTagStr, cls).__new__(cls, value)

    def __init__(self, _value, tag=None, seq=False):
        super(DicomTagStr, self).__init__()
        self._dicom_tag = tag
        self._is_sequence = seq


def parse_tag(name):
    """Parse the given string to determine if it's a property or tag or nested.

    Params:
        name (str|int): The field name or tag value or nested sequence

    Returns:
        DicomTagStr
    """
    if isinstance(name, int):
        tag = pydicom.tag.Tag(name)
        return DicomTagStr(str(tag), tag)

    name = name.strip()
    match = DICOM_TAG_HEX_RE.match(name)
    if match:
        tag = pydicom.tag.Tag(int(name, 16))
        return DicomTagStr(name, tag)

    match = DICOM_TAG_TUPLE_RE.match(name)
    if match:
        tag = pydicom.tag.Tag(int(match.group(1) + match.group(2), 16))
        return DicomTagStr(name, tag)

    match = DICOM_NESTED_RE.match(name)
    if match:
        seq = re.findall(r"([0-9A-Fa-f]{8}|[\w]+|[*])+", name)
        tag_seq = []
        for i, ts in enumerate(seq):
            if i % 2 == 0:  # keyword or tag
                try:  # convert to keyword if possible
                    tag_seq.append(pydicom.datadict.dictionary_keyword(ts))
                except (ValueError, KeyError):
                    tag_seq.append(ts)
            else:  # index of sequence
                try:
                    tag_seq.append(int(ts))
                except ValueError:
                    tag_seq.append(ts)
        return DicomTagStr(name, tag_seq, seq=True)

    return DicomTagStr(name)


class DicomFileProfile(FileProfile):
    """Dicom implementation of load/save and remove/replace fields"""

    name = "dicom"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = ["StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID"]
    regex_compatible = True
    decode = True  # If set to True, will attempt to decode the record upon loading

    def __init__(self):
        super(DicomFileProfile, self).__init__(packfile_type="dicom")

        self.patient_age_from_birthdate = False
        self.patient_age_units = None

        self.remove_private_tags = False

        # set of all lower-cased DICOM keywords, for later validate()
        self.lc_kw_dict = {
            keyword.lower(): keyword
            for keyword in pydicom.datadict.keyword_dict
            if keyword  # non-blank
        }

    def add_field(self, field):
        def expand_tag_list(record, tag_list):
            """Expand wild card sequence in tag_list according to element in dcm"""
            dict_tree = walk_dicom_wild_sequence(record, tag_list)
            return list(dict_paths(dict_tree))

        def deidentify_wild_sequence_field(field, profile, state, record):
            """Find all occurrences by expanding wild card and perform the update"""
            # Replicate field
            dcm_tag = getattr(field.fieldname, "_dicom_tag", None)
            dcm_tags = expand_tag_list(record, dcm_tag)
            for tag in dcm_tags:
                fieldname = DicomTagStr(".".join(map(str, tag)), tag, seq=True)
                tmp_field = DeIdField.factory(
                    {"name": fieldname, field.key: getattr(field, "value", True)}
                )
                tmp_field.deidentify(profile, state, record)

        def deidentify_regex_field(field, profile, state, record):
            """"""
            # Replicate field
            attrs = profile.get_all_record_attributes(record)
            reg = re.compile(field.fieldname)
            for attr in attrs:
                match = reg.match(attr)
                if match:
                    tmp_field = DeIdField.factory(
                        {"name": attr, field.key: getattr(field, "value", True)}
                    )
                    tmp_field.fieldname = parse_tag(attr)
                    tmp_field.deidentify(profile, state, record)

        # Handle tag conversion for later
        field.fieldname = parse_tag(field.fieldname)

        # Patch field.deidentify if '*' is found in sequence
        dcm_tag = getattr(field.fieldname, "_dicom_tag", None)
        is_seq = getattr(field.fieldname, "_is_sequence", False)
        if dcm_tag and is_seq and "*" in dcm_tag:
            field.deidentify = types.MethodType(deidentify_wild_sequence_field, field)

        # Patch field.deidentify if fieldname is regexp
        if getattr(field, "_is_regex", None):
            field.deidentify = types.MethodType(deidentify_regex_field, field)

        super(DicomFileProfile, self).add_field(field)

    def create_file_state(self):
        """Create state object for processing files"""
        return {"series_uid": None, "session_uid": None, "sop_uids": set()}

    def get_dest_path(self, state, record, path):
        """Return default named based on SOPInstanceUID or one based on profile if defined"""
        if not self.filenames:
            # Destination path is sop_uid.modality.dcm
            sop_uid = self.get_value(state, record, "SOPInstanceUID")
            if not sop_uid:
                return path
            modality = self.get_value(state, record, "Modality") or "NA"
            dest_path = "{}.{}.dcm".format(sop_uid, modality.replace("/", "_"))
        else:
            dest_path = super(DicomFileProfile, self).get_dest_path(state, record, path)
        return dest_path

    def get_all_record_attributes(self, record):
        """Returns a list of attributes in the record in a dotty notation format (e.g.
        ``['PatientID', ..., 'AnatomicRegionSequence.0.CodeValue', ...]``
        """
        dotty_attrs = []
        kwlist = sorted(record.dir())
        for kw in kwlist:
            try:
                data_element = record[kw]
                if kw in record and data_element.VR == "SQ":
                    sequence = data_element.value
                    seq_attrs = []
                    for i, ds in enumerate(sequence):
                        attrs = self.get_all_record_attributes(ds)
                        seq_attrs += list(
                            map(lambda x, k=kw, idx=i: f"{k}.{idx}.{x}", attrs)
                        )
                    dotty_attrs += seq_attrs
                else:
                    dotty_attrs.append(kw)
            except Exception:  # pylint: disable=broad-except
                # ignore exceptions when walking context
                continue

        return dotty_attrs

    def to_config(self):
        result = super(DicomFileProfile, self).to_config()

        result["patient-age-from-birthdate"] = self.patient_age_from_birthdate
        if self.patient_age_units:
            result["patient-age-units"] = self.patient_age_units

        result["remove-private-tags"] = self.remove_private_tags

        if self.decode != self.__class__.decode:
            result["decode"] = self.decode

        return result

    def load_config(self, config):
        super(DicomFileProfile, self).load_config(config)

        self.patient_age_from_birthdate = config.get(
            "patient-age-from-birthdate", False
        )
        self.patient_age_units = config.get("patient-age-units")
        self.remove_private_tags = config.get("remove-private-tags", False)
        self.decode = config.get("decode", self.__class__.decode)

    @fw_pydicom_config()
    def load_record(self, state, src_fs, path):  # pylint: disable=too-many-branches
        modified = False
        try:
            with src_fs.open(path, "rb") as f:
                # Extract gzipped dicoms
                _, ext = os.path.splitext(path)
                if ext.lower() == ".gz":
                    f = gzip.GzipFile(fileobj=f)

                # Read and decode the dicom
                dcm = pydicom.dcmread(f, force=True)

                # Remove private tags before decoding
                if self.remove_private_tags:
                    dcm.remove_private_tags()
                    modified = True

                if self.decode:
                    dcm.decode()

                if not dcm.dir():
                    # assuming that a Dicom has at least one known tag
                    raise TypeError("Not a DICOM file")

        except Exception:  # pylint: disable=broad-except
            if not is_dicom(src_fs, path):
                log.warning("IGNORING %s - it is not a DICOM file!", path)
                return None, False
            if self.deid_name != "none":
                log.warning("IGNORING %s - cannot deid an invalid DICOM file!", path)
                return None, False

            log.warning('Packing invalid dicom %s because deid profile is "none"', path)
            return True, False

        # Validate the series/session
        series_uid = dcm.get("SeriesInstanceUID")
        session_uid = dcm.get("StudyInstanceUID")

        if state["series_uid"] is not None:
            # Validate SeriesInstanceUID
            if series_uid != state["series_uid"]:
                log.warning(
                    "DICOM %s has a different SeriesInstanceUID (%s) from the rest of the series: %s",
                    path,
                    series_uid,
                    state["series_uid"],
                )
            # Validate StudyInstanceUID
            elif session_uid != state["session_uid"]:
                log.warning(
                    "DICOM %s has a different StudyInstanceUID (%s) from the rest of the series: %s",
                    path,
                    session_uid,
                    state["session_uid"],
                )
        else:
            state["series_uid"] = series_uid
            state["session_uid"] = session_uid

        # Validate SOPInstanceUID
        sop_uid = dcm.get("SOPInstanceUID")
        if sop_uid:
            if sop_uid in state["sop_uids"]:
                log.error(
                    "DICOM %s re-uses SOPInstanceUID %s, and will be excluded!",
                    path,
                    sop_uid,
                )
                return None, False
            state["sop_uids"].add(sop_uid)

        # Set patient age from date of birth, if specified
        if self.patient_age_from_birthdate:
            dob = dcm.get("PatientBirthDate")
            study_date = dcm.get("StudyDate")

            if dob and study_date:
                try:
                    study_date = datetime.datetime.strptime(
                        study_date, self.date_format
                    )
                    dob = datetime.datetime.strptime(dob, self.date_format)

                    # Max value from dcm.py:84
                    age, units = date_delta(
                        dob,
                        study_date,
                        desired_unit=self.patient_age_units,
                        max_value=960,
                    )
                    dcm.PatientAge = "%03d%s" % (age, units)
                    modified = True
                except ValueError as err:
                    log.debug("Unable to update patient age in file %s: %s", path, err)

        return dcm, modified

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, "wb") as f:
            record.save_as(f)

    def read_field(self, state, record, fieldname):
        # Ensure that value is a string
        dcm_tag = getattr(fieldname, "_dicom_tag", None)
        is_seq = getattr(fieldname, "_is_sequence", False)
        if dcm_tag:
            value = None
            if is_seq:
                value = self._get_field_if_sequence(record, dcm_tag)
            else:
                de = record.get(dcm_tag)
                if de is not None:
                    value = record.get(dcm_tag).value
        else:
            value = getattr(record, fieldname, None)

        if value is not None and not isinstance(value, six.string_types):
            if isinstance(value, collections.Sequence):
                value = ",".join([str(x) for x in value])
            else:  # Unknown value, just convert to string
                value = str(value)
        return value

    def _get_field_if_sequence(self, record, tag):
        """Return data element corresponding to tag"""
        if not len(tag) == 1:
            try:
                return self._get_field_if_sequence(record[tag[0]], tag[1:])
            except (IndexError, KeyError):
                return None
        return record.get(tag[0])

    def _get_or_create_field_if_sequence(self, record, tag):
        """Return DataElement according to tag creating it if does not exist"""
        if not len(tag) == 1:
            try:
                return self._get_or_create_field_if_sequence(record[tag[0]], tag[1:])
            except IndexError:  # extend sequence range
                for _ in range(len(record.value), tag[0] + 1):
                    record.value.append(pydicom.dataset.Dataset())
                return self._get_or_create_field_if_sequence(record[tag[0]], tag[1:])
            except KeyError:  # create sequence
                setattr(record, tag[0], None)
                return self._get_or_create_field_if_sequence(record[tag[0]], tag[1:])
        try:
            return record[tag[0]]
        except KeyError:  # Note: ValueError is raised if tag[0] is not a public tag/keyword
            setattr(record, tag[0], None)
            return record[tag[0]]
        except IndexError:  # extend sequence range
            for _ in range(len(record.value), tag[0] + 1):
                record.value.append(pydicom.dataset.Dataset())

    def remove_field(self, state, record, fieldname):
        dcm_tag = getattr(fieldname, "_dicom_tag", None)
        is_seq = getattr(fieldname, "_is_sequence", False)
        if dcm_tag:
            if is_seq:  # this is a sequence
                self._remove_field_if_sequence(record, dcm_tag)
            elif dcm_tag in record:
                del record[dcm_tag]
        else:
            if hasattr(record, fieldname):
                delattr(record, fieldname)

    def _remove_field_if_sequence(self, record, tag):
        """Remove value on tag list, recursively"""
        if len(tag) == 1:
            if tag[0] in record:
                del record[tag[0]]
        else:
            try:
                self._remove_field_if_sequence(record[tag[0]], tag[1:])
            except (KeyError, ValueError):
                pass

    def replace_field(self, state, record, fieldname, value):
        dcm_tag = getattr(fieldname, "_dicom_tag", None)
        is_seq = getattr(fieldname, "_is_sequence", False)
        if dcm_tag:
            if is_seq:  # this is a sequence
                de = self._get_or_create_field_if_sequence(record, dcm_tag)
                de.value = value
            else:
                try:
                    record[dcm_tag].value = value
                except KeyError:
                    # checking public dictionary to get corresponding VR
                    # if not found, log error and exit until we have a better support
                    # for it
                    try:
                        vr = pydicom.datadict.dictionary_VR(dcm_tag)
                    except KeyError:
                        log.error(
                            f"Invalid replace-with action. Unknown VR for tag {dcm_tag}."
                        )
                        sys.exit(1)
                    record.add_new(dcm_tag, vr, value)
        else:
            setattr(record, fieldname, value)

    def validate_filenames(self, errors):
        """Validate the filename section of the profile,

        Args:
            errors (list): Current list of error message

        Returns:
            (list): Extended list of errors message
        """

        for filename in self.filenames:
            group_names = []
            if filename.get("input-regex"):  # check regexp
                try:
                    regex = re.compile(filename.get("input-regex"))
                    group_names = [x.lower() for x in regex.groupindex.keys()]
                except re.error:
                    # errors got log already in superclass method, still needs group_names for following validation
                    continue

            # check group do not collide with dicom keyword
            lc_kw_list = list(self.lc_kw_dict.keys())
            for grp in group_names:
                if grp in lc_kw_list:
                    errors.append(
                        f"regex group {grp} must be unique. Currently colliding with Dicom keywords"
                    )

            # check output filename keyword are valid
            kws = re.findall(r"\{([^}]+)\}", filename["output"])
            lc_kw_list = list(self.lc_kw_dict.keys()) + group_names
            for kw in kws:
                lc_kw = kw.lower()
                if lc_kw not in lc_kw_list:
                    errors.append(
                        f"Filename output invalid. Group not in Dicom keyword or in regex groups: {kw}"
                    )

        return errors

    @fw_pydicom_config()
    def process_files(self, *args, **kwargs):
        super(DicomFileProfile, self).process_files(*args, **kwargs)

    def _validate_replace_with(self, field, errors):
        with tempfile.TemporaryFile() as fp:
            fp.is_little_endian = True
            fp.is_implicit_VR = False
            try:
                vr = pydicom.datadict.dictionary_VR(field.fieldname)
                de = pydicom.DataElement(field.fieldname, vr, field.value)
                writer_function, writer_param = writers[vr]
                if vr in text_VRs or vr in ("PN", "SQ"):
                    writer_function(fp, de)
                else:
                    # Many numeric types use the same writer but with
                    # numeric format parameter
                    if writer_param is not None:
                        writer_function(fp, de, writer_param)
                    else:
                        writer_function(fp, de)
            except Exception:
                errors.append(
                    f"Incorrect value type for Dicom element {field.fieldname} (VR={vr}): {type(field.value).__name__}"
                )

    def _validate_hash(self, field, errors):
        """Validate that VR of data element is string compatible"""
        vr = pydicom.datadict.dictionary_VR(field.fieldname)
        if vr in [
            "AT",
            "FL",
            "FD",
            "OB",
            "OW",
            "OF",
            "SL",
            "SQ",
            "SS",
            "UL",
            "UN",
            "US",
            "OB/OW",
            "OW/OB",
            "OB or OW",
            "OW or OB",
        ]:
            errors.append(
                f"{field.fieldname} cannot be hashed - VR not compatible ({vr})"
            )

    def validate(self, enhanced=False):
        """Validate the profile, returning any errors.

        Args:
            enhanced (bool): If True, test profile execution on a set of test files

        Returns:
            list(str): A list of error messages, or an empty list
        """

        errors = super(DicomFileProfile, self).validate()

        if self.filenames:
            self.validate_filenames(errors)

        for field in self.fields:
            if field.fieldname.startswith(self.filename_field_prefix) or getattr(
                field, "_is_regex"
            ):
                continue
            # do not validate if name is a tag or nested
            if (
                DICOM_TAG_HEX_RE.match(field.fieldname)
                or DICOM_TAG_TUPLE_RE.match(field.fieldname)
                or DICOM_NESTED_RE.match(field.fieldname)
            ):
                continue
            lc_field = field.fieldname.lower()
            if lc_field not in self.lc_kw_dict:
                errors.append("Not in DICOM keyword list: " + field.fieldname)
            # case difference; correct to proper DICOM spelling
            elif field.fieldname != self.lc_kw_dict[lc_field]:
                field.fieldname = self.lc_kw_dict[lc_field]

            # validate action specifics
            if field.fieldname.lower() in self.lc_kw_dict:
                if field.key == "replace-with":
                    self._validate_replace_with(field, errors)
                if field.key == "hash":
                    self._validate_hash(field, errors)

        if enhanced:
            # Test deid profile on test Dicom files
            test_files = get_testdata_files("*.dcm")
            for test_file in test_files:
                dirname, basename = os.path.split(test_file)
                basename = six.u(basename)  # fs requires unicode
                if basename == "1.3.6.1.4.1.5962.1.1.0.0.0.977067309.6001.0.OT.dcm":
                    continue  # this test file seems to be corrupted
                test_fs = OSFS(dirname)
                try:
                    self.process_files(test_fs, test_fs, [basename])
                except Exception:
                    log.error(
                        "Failed to run profile on pydicom test file %s",
                        basename,
                        exc_info=True,
                    )
                    raise

        return errors
