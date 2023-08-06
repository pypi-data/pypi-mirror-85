"""Provides DicomScanner class."""

import copy
import gzip
import itertools
import logging
import os
import typing
from pathlib import Path

import fs
from flywheel_migration.dcm import DicomFile
from pydicom.datadict import tag_for_keyword
from pydicom.tag import Tag

from ... import util
from .. import deid, errors
from .. import schemas as T
from .abstract import AbstractScanner

log = logging.getLogger(__name__)


class DicomScanner(AbstractScanner):
    """Scanner class to scan dicom files and create appropriate ingest items."""

    scanner_type = "dicom"
    # The session label dicom header key
    session_label_key = "StudyDescription"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("context", {})
        super().__init__(*args, **kwargs)
        self.related_acquisitions = False
        self.sessions = {}
        self.deid_profile = None

        if self.ingest_config.de_identify:
            # inizialize deid profile
            self.deid_profile = deid.load_deid_profile(
                self.ingest_config.deid_profile,
                self.ingest_config.deid_profiles,
            ).get_file_profile("dicom")

        self.get_subject_code = None
        if self.ingest_config.subject_config:

            def get_subject_code(dcm):
                fields = [
                    str(dcm.get(field, "")).strip().lower()
                    for field in self.ingest_config.subject_config.map_keys
                ]
                return self.get_subject_code_fn(fields)

            self.get_subject_code = get_subject_code

        self.dicom_utils = util.DicomUtils(
            deid_profile=self.deid_profile, get_subject_code_fn=self.get_subject_code
        )

    def _scan(self, subdir):
        """Scan all files in the given walker"""
        tags = [
            Tag(tag_for_keyword(keyword)) for keyword in self.dicom_utils.required_tags
        ]

        for fileinfo in self.iter_files(subdir, report_progress=True):
            filepath = fs.path.combine(subdir, fileinfo.name)
            with self.walker.open(
                filepath, "rb", buffering=self.worker_config.buffer_size
            ) as fileobj:
                try:
                    self.scan_dicom_file(filepath, fileobj, tags, size=fileinfo.size)
                except (ValueError, util.InvalidLabel) as exc:
                    log.debug(f"Skipped file {filepath} because {str(exc)}")
                    self.file_errors.append(
                        T.Error(
                            code=errors.InvalidDicomFile.code,
                            message=str(exc),
                            filepath=filepath,
                        )
                    )

        # TODO: consider memory usage in case of huge dataset
        for session in self.sessions.values():
            session_context = copy.deepcopy(self.context)
            session_context.update(session.context)

            session_uid = session.context["session"]["uid"]

            for acquisition in itertools.chain(
                session.acquisitions.values(), session.secondary_acquisitions.values()
            ):
                acquisition_context = copy.deepcopy(session_context)
                acquisition_context.update(acquisition.context)

                series_uid = acquisition.context["acquisition"]["uid"]

                for series_uid, files in acquisition.files.items():
                    size = 0
                    file_paths = []
                    for sop_uid, sop_files in acquisition.files[series_uid].items():
                        size += sum([filesize for _, filesize in sop_files])
                        file_paths.extend(
                            [fs.path.relpath(filepath) for filepath, _ in sop_files]
                        )
                    common_path = Path(os.path.commonpath(file_paths)).as_posix()
                    file_paths = [
                        Path(f).relative_to(common_path).as_posix() for f in file_paths
                    ]
                    filename = acquisition.filenames.get(series_uid)

                    packfile_context = copy.deepcopy(acquisition_context)
                    packfile_context["packfile"] = {
                        "type": "dicom",
                        "flatten": True,
                    }

                    item_with_uids = T.ItemWithUIDs(
                        item=T.Item(
                            type="packfile",
                            dir=common_path,
                            files=file_paths,
                            filename=filename,
                            files_cnt=len(files),
                            bytes_sum=size,
                            context=packfile_context,
                        ),
                        uids=[],
                    )

                    for sop_uid in files:
                        acquisition_number = acquisition.acquisition_number

                        for file in files[sop_uid]:
                            item_with_uids.uids.append(
                                T.UIDIn(
                                    item_id=item_with_uids.item.id,
                                    study_instance_uid=session_uid,
                                    series_instance_uid=series_uid,
                                    acquisition_number=acquisition_number,
                                    sop_instance_uid=sop_uid,
                                    filename=file[0],
                                )
                            )

                    yield item_with_uids

    def scan_dicom_file(self, path, fp, tags, size=0):
        """Scan a single dicom file

        Args:
            path   (str): File path
            fp     (BinaryIO): File like object
            tags   (list): Dicom tags
            walker (AbstractWalker): Filesystem walker object

        """
        _, ext = os.path.splitext(path)
        if ext.lower() == ".gz":
            fp = gzip.GzipFile(fileobj=fp)

        # Don't decode while scanning, stop as early as possible
        # TODO: will we ever rely on fields after stack id for subject mapping
        if self.related_acquisitions:
            stop_function = stop_at_key((0x3006, 0x0011))
        else:
            stop_function = stop_at_key((0x0020, 0x9056))

        dcm = DicomFile(
            fp,
            parse=False,
            session_label_key=self.session_label_key,
            decode=self.related_acquisitions,
            stop_when=stop_function,
            update_in_place=False,
            specific_tags=tags,
            force=util.is_dicom_file(path),
        )

        acquisition = self.resolve_acquisition(self.context, dcm)
        series_uid = self.dicom_utils.get_value(dcm, "SeriesInstanceUID", required=True)
        sop_uid = self.dicom_utils.get_value(dcm, "SOPInstanceUID", required=True)
        acquisition_number = self.dicom_utils.get_value(dcm, "AcquisitionNumber")
        if acquisition_number and int(acquisition_number) > 1:
            acquisition.acquisition_number = acquisition_number
            # it causes problems with packfiles, so skipping for now
            # series_uid = f"{series_uid}_{int(acquisition_number)}"

        acquisition.files.setdefault(series_uid, {})
        acquisition.files[series_uid].setdefault(sop_uid, [])
        acquisition.files[series_uid][sop_uid].append((path, size))

        if series_uid not in acquisition.filenames:
            acquisition_timestamp = self.dicom_utils.determine_acquisition_timestamp(
                dcm
            )
            series_label = self.dicom_utils.determine_acquisition_label(
                acquisition.context,
                dcm,
                series_uid,
                timestamp=acquisition_timestamp,
            )
            filename = self.dicom_utils.determine_dicom_zipname(
                acquisition.filenames, series_label
            )
            acquisition.filenames[series_uid] = filename

    def resolve_session(self, context, dcm):
        """Find or create a sesson from a dcm file. """
        subject_code = self.dicom_utils.determine_subject_code(context, dcm)

        session_uid = self.dicom_utils.get_value(dcm, "StudyInstanceUID", required=True)
        if session_uid not in self.sessions:
            session_timestamp = self.dicom_utils.get_timestamp(
                dcm, "StudyDate", "StudyTime"
            )

            # Create session
            session_context = {
                **{
                    "uid": session_uid,
                    "label": self.dicom_utils.determine_session_label(
                        context, dcm, session_uid, timestamp=session_timestamp
                    ),
                    "timestamp": session_timestamp,
                    "timezone": str(util.DEFAULT_TZ),
                },
                **self.context.get("session", {}),
            }
            subject_context = {
                **{"label": subject_code},
                **self.context.get("subject", {}),
            }
            self.sessions[session_uid] = DicomSession(
                {
                    "session": session_context,
                    "subject": subject_context,
                }
            )

        return self.sessions[session_uid]

    def resolve_acquisition(self, context, dcm):
        """Find or create an acquisition from a dcm file. """
        session = self.resolve_session(context, dcm)
        series_uid = self.dicom_utils.get_value(dcm, "SeriesInstanceUID", required=True)
        primary_acquisition_file = True

        if self.related_acquisitions and dcm.get("ReferencedFrameOfReferenceSequence"):
            # We need to add it to the acquisition of the primary series uid
            try:
                series_uid = (
                    dcm.get("ReferencedFrameOfReferenceSequence")[0]
                    .get("RTReferencedStudySequence")[0]
                    .get("RTReferencedSeriesSequence")[0]
                    .get("SeriesInstanceUID")
                )
                primary_acquisition_file = False
            except (TypeError, IndexError, AttributeError):
                log.warning(
                    "Unable to find related series for file {}. Uploading into its own acquisition"
                )

        acquisition_number = self.dicom_utils.get_value(dcm, "AcquisitionNumber")
        if acquisition_number and int(acquisition_number) > 1:
            # it causes problems with packfiles, so skipping for now
            # series_uid = f"{series_uid}_{int(acquisition_number)}"
            pass

        if series_uid not in session.acquisitions:
            # full acquisition doesn't exists
            if (
                not primary_acquisition_file
                and series_uid in session.secondary_acquisitions
            ):
                # The secondary acquisition exists
                return session.secondary_acquisitions[series_uid]

            acquisition_timestamp = self.dicom_utils.determine_acquisition_timestamp(
                dcm
            )
            acquisition_context = {
                **{
                    "uid": series_uid,
                    "label": self.dicom_utils.determine_acquisition_label(
                        context, dcm, series_uid, timestamp=acquisition_timestamp
                    ),
                    "timestamp": acquisition_timestamp,
                    "timezone": str(util.DEFAULT_TZ),
                },
                **self.context.get("acquisition", {}),
            }
            acquisition = DicomAcquisition(
                {"acquisition": acquisition_context},
                acquisition_number=acquisition_number,
            )

            if primary_acquisition_file:
                # Check for a secondary and add it the files and filenames to the primary
                if series_uid in session.secondary_acquisitions:
                    acquisition.files = session.secondary_acquisitions.get(
                        series_uid
                    ).files
                    acquisition.filenames = session.secondary_acquisitions.pop(
                        series_uid
                    ).filenames

                session.acquisitions[series_uid] = acquisition
                return session.acquisitions[series_uid]
            session.secondary_acquisitions[series_uid] = acquisition
            return session.secondary_acquisitions[series_uid]

        # Acquisition already exists
        return session.acquisitions[series_uid]


class DicomSession:
    """Dicom session class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, context):
        """Helper class that holds session properties and acquisitions"""
        self.context = context
        self.acquisitions = {}
        self.secondary_acquisitions = {}  # Acquisitions that we don't have all
        # of the info for yet


class DicomAcquisition:
    """Dicom acquisition class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, context, acquisition_number=None):
        """Helper class that holds acquisition properties and files"""
        self.context = context
        self.files = (
            {}
        )  # Map of primary_series_uids to maps of series uids to filepaths
        # So that the primary series uid can be used to group multiple dicom series into one acquisition
        self.filenames = {}  # A map of series uid to filenames
        self.acquisition_number = acquisition_number


def stop_at_key(key: typing.Any):
    """Return stop_when function for given DICOM tag"""
    stop_tag = Tag(key)

    def stop_when(tag: Tag, *_):
        """Return True if the current tag equals the stop_tag"""
        return tag == stop_tag

    return stop_when
