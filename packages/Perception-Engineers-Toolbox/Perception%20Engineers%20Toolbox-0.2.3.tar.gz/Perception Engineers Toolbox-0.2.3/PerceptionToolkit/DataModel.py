import numpy as np
import tabel as tb
from typing import Dict, Union, Sequence
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from enum import Enum, IntEnum, auto
import copy


class DataModel:
    """Holds all the data that can be associated with one recording.

    Attributes:
        raw: the raw data matrix containing all the data associated with the recording (i.e., raw measurement samples).
            You likely don't want to access those directly, unless fast write access to the data is required. Use the
            DataModel's accessors (time(), x(), y(), pupil_diameter(), etc.) instead.
            Data is held in a Tabel datastructure. That is a thin wrapper around numpy columns and enables us to have
            numpy's quick indexing access and a column access similar to pandas (without its slow chained indexing that
            copies stuff uncontrollably whenever it feels like it). When setting this, make sure to provide your
            timestamps in milliseconds. Please remember to perform a deep copy before you modify slices of this data!
        events: Eye movement events detected via an event detection algorithm. You need to run such a method before any
            data is available. Contains the event data in three columns:
            The type of eye movement (fixation / saccade/ ...) according to EyeMovementTypes; The index of event start
            as a row index to the raw data matrix (inclusive); the index of event end (inclusive).
            You might prefer to access event data via the fix = data.fixations() function and to cast each row to a
            Fixation object via EyeMovements.Fixation(data, fix[:,1], fix[:,2])
        metrics: After calculation of specific metrics, these can be made available by their name by placing them in the
            metrics variable (e.g., average fixation duration,...)
        meta: Meta information of any kind on the recording. The META Enumeration contains popular instances.
        accessors: keeps track of the most important columns of an eye-tracking recording, such as the coordinates of
            point of regard, the timestamp column and the data validity columns.
            This is required as these fields are often named very different by manufacturers and across data formats
            and devices. To make access to these values easy and universal, point these variables to the column of your
            dataset where the respective information is contained.
            This is also done during CSV import, e.g., via the PersistenceCSV plugin. By placing an "alias" we do
            not have to rename the columns and can keep them as they are in the original file. When exporting data that
            should be easily reimported, make sure to write down the accessors alongside with the data and to import and
            set them as well. The enum ET keeps track of fields we want to have available as standard fields. Note that
            not all of them have to be set/available, and you might very well get no result when querying them.
    """

    class ET(IntEnum):
        """
        Defines some constants that name the common columns in an eye-tracking data format.
        As they are named differently by each manufacturer, we alias them via these accessors to provide the identical
        interface for each protocol/device. Not each protocol is guaranteed to provide all of these (e.g., some
        eye-trackers are monocular only).

        TIME Timestamp in milliseconds (floating point format to represent also fractions of milliseconds).
        LEFT_EYE_X The horizontal gaze (=PoR) coordinate of the left eye of the subject.
        LEFT_EYE_Y The vertical gaze (=PoR) coordinate of the left eye of the subject
        LEFT_EYE_VALID Whether the eye-tracker rates this sample as reliable or not.
        LEFT_PUPIL_DIAMETER Diameter of the pupil circle (in mm, if available. Some protocols might implement pixels though).
        RIGHT_... The same for the subject's right eye.

        EVENT_TYPE The encoded event type identifier (fixation/saccade) according to EyeMovementTypes.
        EVENT_IDX Sequential numbering of eye movements, where each movement gets its own, unique id. These two are used
            when importing eye movement data that already contains event detection data.
        """
        TIME = auto()
        LEFT_EYE_X = auto()
        LEFT_EYE_Y = auto()
        LEFT_EYE_VALID = auto()
        LEFT_PUPIL_DIAMETER = auto()
        RIGHT_EYE_X = auto()
        RIGHT_EYE_Y = auto()
        RIGHT_EYE_VALID = auto()
        RIGHT_PUPIL_DIAMETER = auto()

        EVENT_TYPE = auto()
        EVENT_IDX = auto()

        @staticmethod
        def to_ET(s: str):
            d: Dict[str, DataModel.ET] = {"TIME": DataModel.ET.TIME,
                                          "LEFT_EYE_X": DataModel.ET.LEFT_EYE_X,
                                          "LEFT_EYE_Y": DataModel.ET.LEFT_EYE_Y,
                                          "LEFT_EYE_VALID": DataModel.ET.LEFT_EYE_VALID,
                                          "LEFT_PUPIL_DIAMETER": DataModel.ET.LEFT_PUPIL_DIAMETER,
                                          "RIGHT_EYE_X": DataModel.ET.RIGHT_EYE_X,
                                          "RIGHT_EYE_Y": DataModel.ET.RIGHT_EYE_Y,
                                          "RIGHT_EYE_VALID": DataModel.ET.RIGHT_EYE_VALID,
                                          "RIGHT_PUPIL_DIAMETER": DataModel.ET.RIGHT_PUPIL_DIAMETER,
                                          "EVENT_TYPE": DataModel.ET.EVENT_TYPE,
                                          "EVENT_IDX": DataModel.ET.EVENT_IDX}
            assert (s in d)
            return d[s]

    class META(Enum):
        """
        Defines some constants that name the common columns in an eye-tracking data format.

        TRIAL_NUMBER The number that uniquely identifies a trial
        SUBJECT The id/name/codeword of a subject
        LABEL A group/condition identifier
        STIMULUS The displayed stimulus material (e.g., name, filename, url, id)
        CUSTOM Can be used to implement custom functionality. The program core does not ensure anything for this type.
        """
        TRIAL_NUMBER = auto()
        SUBJECT = auto()
        LABEL = auto()
        STIMULUS = auto()
        CUSTOM = auto()

        @staticmethod
        def to_META(s: str):
            d: Dict[str, DataModel.META] = {"TRIAL": DataModel.META.TRIAL_NUMBER, "SUBJECT": DataModel.META.SUBJECT,
                                            "LABEL": DataModel.META.LABEL, "STIMULUS": DataModel.META.STIMULUS}
            assert (s in d)
            return d[s]

    accessors: Dict[ET, str] = {}

    # The DataModel will by default use the average eye for all calculations (if only one eye is considered valid, it
    # will use only that eye). If you set the dominant eye, the dominant eye only will be used instead (except if its
    # sample is marked invalid; in that case the non-dominant eye will replace it).
    dominant_eye: str = ""  # any of ["Left", "Right", ""] to use left / right / average eye

    def __init__(self):
        self.events = np.empty([0, 0, 0])  # type, start, stop
        self.metrics = {}
        self.meta: Dict[DataModel.META, Union[str, int, float]] = {}
        self.raw = tb.Tabel()
        self.accessors = {}
        self.dominant_eye = ""

    def time(self):
        """The timestamp in [ms]"""
        return self.raw[self.accessors[DataModel.ET.TIME]]

    def x(self):
        """The X-Coordinate of the point of regard (= gaze location)
        This function will return
        - the coordinate of the dominant eye, if set and valid.
        - the average eye, if both eyes are valid and no dominant eye is set.
        - the coordinate of the valid eye in case one eye is invalid.
        """
        return self.__select_parameter(DataModel.ET.LEFT_EYE_X, DataModel.ET.RIGHT_EYE_X)

    def y(self):
        """The Y-Coordinate of the point of regard (= gaze location)
        This function will return
        - the coordinate of the dominant eye, if set and valid.
        - the average eye, if both eyes are valid and no dominant eye is set.
        - the coordinate of the valid eye in case one eye is invalid.
        """
        return self.__select_parameter(DataModel.ET.LEFT_EYE_Y, DataModel.ET.RIGHT_EYE_Y)

    def pupil_diameter(self):
        """The pupil diameter
        This function will return
        - the PD of the dominant eye, if set and valid.
        - the average eye, if both eyes are valid and no dominant eye is set.
        - the PD of the valid eye in case one eye is invalid.
        """
        return self.__select_parameter(DataModel.ET.LEFT_PUPIL_DIAMETER, DataModel.ET.RIGHT_PUPIL_DIAMETER)

    def valid(self):
        """Validity information on the gaze signal. Is either of (False, True).
        Is there valid gaze information available for any of the two eyes (logical or)?
        """
        return self.__any_selection(DataModel.ET.LEFT_EYE_VALID, DataModel.ET.RIGHT_EYE_VALID)

    def get(self, idx: ET):
        """
        Get the data of a specific accessor. This is the preferred way of accessing raw data across protocols.
        Please consider using time(), x() and y() instead, in case you do not want to care about some internals such as
        dominant eye selection, valid eye selection and average eye calculations.
        """
        if idx in self.accessors:
            return self.raw[self.accessors[idx]]
        else:
            return None

    def get_by_name(self, column_name: str):
        """Provides column-wise access to the raw data matrix via the string provided in the header line of the
        recording file. If possible, use the aliased functions via accessors instead to enable cross-protocol
        compatibility of your functions. It will make them "immune" to the exact file format loaded."""
        if column_name in self.raw.columns:
            return self.raw[column_name]
        else:
            return None

    def sample_count(self) -> int:
        """The number of total samples (= individual measurement points) contained in the recording"""
        return self.time().size

    # in ms
    def duration(self) -> float:
        """The timespan covered by the recording in [ms]"""
        return self.time()[-1] - self.time()[0]

    # samples per second
    def sampling_frequency(self) -> float:
        """The average number of samples recorded per second of the recording (= fps or Hz). This value is only
        useful/accurate for relatively constant recording rates. """
        assert self.sample_count() > 0
        assert self.duration() > 0
        return self.sample_count() / self.duration() * 1000

    def ms_per_frame(self) -> float:
        """The number of milliseconds the recording device required on average to record a single sample. This value
        is only useful/accurate for relatively constant recording rates. """
        assert self.sample_count() > 0
        return 1000.0 / self.sampling_frequency()

    def fixations(self):
        """Provides access to all fixations detected in the data after an event detection method was run.

        Returns:
            Contains the event data in three columns:
            The type of eye movement (fixation / saccade/ ...); The index of event start as a row index to the raw data
            matrix (inclusive); the index of event end (inclusive).
            You might prefer to access event data via the fix = data.fixations() function and to cast each row to a
            Fixation object via EyeMovements.Fixation(data, fix[i,1], fix[i,2])
        """
        return self.events_of_type(EyeMovementTypes.FIXATION)

    def saccades(self):
        """Provides access to all saccades detected in the data after an event detection method was run.

        Returns:
            Contains the event data in three columns:
            The type of eye movement (fixation / saccade/ ...); The index of event start as a row index to the raw data
            matrix (inclusive); the index of event end (inclusive).
            You might prefer to access event data via the sacc = data.saccades() function and to cast each row to a
            Saccade object via EyeMovements.Saccade(data, fix[i,1], fix[i,2])
        """
        return self.events_of_type(EyeMovementTypes.SACCADE)

    def events_of_type(self, event_type: EyeMovementTypes) -> np.array:
        """ Works exactly as fixations() or saccades() but allows to get any type of movement."""
        if self.events.size == 0:
            return self.events
        assert self.events.shape[0] > 0
        return self.events[self.events[:, 0] == event_type, :]

    def remove_all_events_of_type(self, event_types: Sequence[EyeMovementTypes]) -> int:
        """ Allows to delete certain kinds of detections, e.g., for re detection with different methods / parameters.
        Typically used within Eventdetection plugins to clear any previously detected eye movements of the same type."""
        if self.events.size == 0:
            return 0
        
        matches = np.isin(self.events[:, 0], event_types)
        self.events = self.events[np.logical_not(matches), :]
        return np.sum(matches)

    def test_events_consistency(self):
        """Checks whether there are overlapping events.

        Should be called at the end of event detection, as long as events are mutually exclusive (e.g., saccades and
        fixations).
        Do not call this after events are supposed to be overlapping (e.g., detecting microsaccades within fixations)

        Will fail with an assertion, if something goes wrong.
        """
        for i in range(0, self.events.shape[0]):
            for j in range(i + 1, self.events.shape[0]):
                e1 = self.events[i, :]
                e2 = self.events[j, :]
                assert (not ((e2[1] <= e1[1] <= e2[2]) or (e2[1] <= e1[2] <= e2[2])))

    def __dominance_selection(self, first: ET, second: ET, first_valid: ET, second_valid: ET):
        x = copy.deepcopy(self.raw[self.accessors[first]])
        if second in self.accessors and second_valid in self.accessors:
            # By testing for <>0.6 we can allow confidence values as well.
            v = np.logical_and(self.raw[self.accessors[first_valid]] < 0.6,
                               self.raw[self.accessors[second_valid]] > 0.6)
            x[v] = self.raw[self.accessors[second]][v]
        return x

    def __average_selection(self, first: ET, second: ET, first_valid: ET, second_valid: ET):
        x1 = self.raw[self.accessors[first]]
        x2 = self.raw[self.accessors[second]]
        v1 = self.raw[self.accessors[first_valid]] < 0.6
        v2 = self.raw[self.accessors[second_valid]] < 0.6
        x = copy.deepcopy(self.raw[self.accessors[first]])
        x[np.logical_not(v1)] = x2[np.logical_not(v1)]
        x[np.logical_and(v1, v2)] = (x1[np.logical_and(v1, v2)] + x2[np.logical_and(v1, v2)]) / 2.0
        return x

    def __any_selection(self, first_valid: ET, second_valid: ET):
        if first_valid in self.accessors and second_valid in self.accessors:
            x1 = self.raw[self.accessors[first_valid]] > 0.6
            x2 = self.raw[self.accessors[second_valid]] > 0.6
            return np.logical_or(x1, x2)
        if first_valid in self.accessors:
            return self.raw[self.accessors[first_valid]] > 0.6
        if second_valid in self.accessors:
            return self.raw[self.accessors[second_valid]] > 0.6
        assert False

    def __select_parameter(self, left: ET, right: ET):
        """
        Use the dominant eye, if present and valid
            use the non-dominant eye, if not valid
        Use the eye present, if only one is present
        Use the average of both eyes, if both are present and valid
            Use the one valid if one of them is invalid
            """

        if self.dominant_eye:
            if self.dominant_eye == "Left":
                return self.__dominance_selection(left, right, DataModel.ET.LEFT_EYE_VALID,
                                                  DataModel.ET.RIGHT_EYE_VALID)
            if self.dominant_eye == "Right":
                return self.__dominance_selection(right, left, DataModel.ET.RIGHT_EYE_VALID,
                                                  DataModel.ET.LEFT_EYE_VALID)
        if left in self.accessors and right in self.accessors:
            return self.__average_selection(left, right, DataModel.ET.LEFT_EYE_VALID, DataModel.ET.RIGHT_EYE_VALID)
        if left in self.accessors:
            return self.raw[self.accessors[left]]
        if right in self.accessors:
            return self.raw[self.accessors[right]]
        assert False
