from PerceptionToolkit.PluginInterfaces import IPersistencePlugin
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from typing import List, Any, Dict, Sequence
import tabel as tb
import pandas as pd
import csv
import os.path
import PerceptionToolkit.EyeMovementTypes


class PersistenceCSV(IPersistencePlugin):
    """Import a text file
        (Uses pandas as backend because it offers quite stable and nicely performing import and conversion routines)

    Attributes:
        filename: Which file to load. Can be relative or absolute path.
        preset: Instead of tediously specifying the parameters for CSV import, you can also select from a preset of
            common formats, including Tobii and SMI exports.
        separator: The character(sequence) that delimits individual entries in the file
        skip_header_lines: The number of lines at the beginning of the file that should be completely skipped.
            This does not include the actual table header (i.e., the line that provides names for the data columns).
        comment_symbol: a symbol that marks lines which should be ignored. Must be the first character in that line.
        trial_split_symbol: When loading multiple trials from one file, this symbol marks the beginning of a new trial.
            May occur anywhere within the file.
        trial_column: The column name that specifies the trial uniquely. May be a number or the stimulus name. A
            Recording will be split when the entry at this column changes value.
        timestamp_to_ms_factor: In case the timestamp is not provided in units of milliseconds, this is the conversion
            factor that should be applied. E.g., 0.001 to convert from microseconds to milliseconds. We handle
            timestamps as floats and can therefore also represent fractions of milliseconds so don't worry about a loss
            of precision of the timestamp.
        confidence_min: In case the file provides a confidence value for pupil detection / gaze estimation, this is the
            minimum confidence at which a sample is rated as trustworthy (often about 0.6, e.g., PupilLabs/EyeRecToo).
            Can be set to PersistenceCSV.VALIDITY_DISABLED to disable this check, in case the value is not available.
        confidence_max: In case the file provides a confidence value for pupil detection / gaze estimation, this is the
            maximum confidence at which a sample is rated as trustworthy (in case e.g. 0 means good and 1 means bad).
            Can be set to PersistenceCSV.VALIDITY_DISABLED to disable this check, in case the value is not available.
        invalid_value: In case your file does not provide a validity or confidence measure, invalid samples might still
            be identified by their value (e.g., 0.0 or -999). Can be set to PersistenceCSV.VALIDITY_DISABLED in case you
            do not want to use this check.
        aliases: As each file names their columns differently (e.g., X, L[X], PoR_X,...) the aliases can be used to tell
            which columns contain the LX, LY, Time, Valid data. You need to set these in order to be able to use your
            data.
        target_files: file names for the export in the order in which the DataModels are contained (first data entry
            will receive first file name). When setting this parameter, each recording will be exported to its own file.

    Note:
        The CSV importer may add a column named "left eye valid" and "right eye valid" to the data, in case no validity
        column is specified. The reported number of columns loaded from file may therefore exceed the number of columns
        present in the file by up to 2.
    """

    VALIDITY_DISABLED: int = -91827  # some random value that is unlikely to appear in reality

    def __init__(self):
        super(PersistenceCSV, self).__init__()
        self.filename: str = ""
        self.separator: str = " "
        self.skip_header_lines: int = 0
        self.comment_symbol: str = "#"
        self.trial_split_symbol = ""
        self.trial_column = ""
        self.timestamp_to_ms_factor: float = 1.0
        self.preset = ""

        self.confidence_min: float = PersistenceCSV.VALIDITY_DISABLED
        self.confidence_max: float = PersistenceCSV.VALIDITY_DISABLED
        self.invalid_value: float = PersistenceCSV.VALIDITY_DISABLED

        self.aliases: Dict[str, str] = {}

        self.target_files = []

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.filename = parameters.get("filename", self.filename)

        presets = {"Tobii": self.preset_tobii,
                   "SMI": self.preset_smi,
                   "EyeRecToo": self.preset_eyerectoo}

        if "preset" in parameters.keys():
            if parameters["preset"] in presets:
                presets[parameters["preset"]]()
            else:
                print("WARNING! Preset not found." + parameters["preset"])

        # this also allows for modifications of the presets! TODO We should probably warn if someone does that
        self.separator = parameters.get("separator", self.separator)
        self.skip_header_lines = parameters.get("skip_header_lines", self.skip_header_lines)
        self.comment_symbol = parameters.get("comment_symbol", self.comment_symbol)
        self.timestamp_to_ms_factor = parameters.get("timestamp_to_ms_factor", self.timestamp_to_ms_factor)
        self.trial_split_symbol = parameters.get("trial_split_symbol", self.trial_split_symbol)
        self.trial_column = parameters.get("trial_column", self.trial_column)
        self.confidence_min = parameters.get("confidence_min", self.confidence_min)
        self.confidence_max = parameters.get("confidence_max", self.confidence_max)
        self.invalid_value = parameters.get("invalid_value", self.invalid_value)

        self.aliases = parameters.get("aliases", self.aliases)

        self.target_files = parameters.get("target_files", self.target_files)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    @staticmethod
    def ensure_float_format(model: pd.DataFrame, idx: str):
        # Pandas is able to convert even if some values are non-convertible. They will be nan then.
        model[idx] = pd.to_numeric(model[idx], errors="coerce")

    def post_process(self, model: DataModel) -> None:
        # scale time dimension to ms
        model.raw[model.accessors[DataModel.ET.TIME]] = model.get(DataModel.ET.TIME) * self.timestamp_to_ms_factor

        # if no validity is provided, append a column
        if DataModel.ET.LEFT_EYE_VALID not in model.accessors and (
                DataModel.ET.LEFT_EYE_X in model.accessors or DataModel.ET.LEFT_EYE_Y in model.accessors):
            model.raw["left eye valid"] = np.ones(model.raw.shape[0])
            model.accessors[DataModel.ET.LEFT_EYE_VALID] = "left eye valid"
        if DataModel.ET.RIGHT_EYE_VALID not in model.accessors and (
                DataModel.ET.RIGHT_EYE_X in model.accessors or DataModel.ET.RIGHT_EYE_Y in model.accessors):
            model.raw["right eye valid"] = np.ones(model.raw.shape[0])
            model.accessors[DataModel.ET.RIGHT_EYE_VALID] = "right eye valid"
        # mark validity as either 0 or 1
        if not self.confidence_min == PersistenceCSV.VALIDITY_DISABLED:
            model.raw[model.accessors[DataModel.ET.LEFT_EYE_VALID]] = \
                model.get(DataModel.ET.LEFT_EYE_VALID) >= self.confidence_min
            model.raw[model.accessors[DataModel.ET.RIGHT_EYE_VALID]] = \
                model.get(DataModel.ET.RIGHT_EYE_VALID) >= self.confidence_min
        if not self.confidence_max == PersistenceCSV.VALIDITY_DISABLED:
            model.raw[model.accessors[DataModel.ET.LEFT_EYE_VALID]] = \
                model.get(DataModel.ET.LEFT_EYE_VALID) <= self.confidence_min
            model.raw[model.accessors[DataModel.ET.RIGHT_EYE_VALID]] = \
                model.get(DataModel.ET.RIGHT_EYE_VALID) <= self.confidence_min
        if not self.invalid_value == PersistenceCSV.VALIDITY_DISABLED:
            # this is a bit more complex as we have to look for invalid values in any of the eyes and any of X/Y

            if DataModel.ET.LEFT_EYE_X in model.accessors and DataModel.ET.LEFT_EYE_Y in model.accessors:
                left_valid = np.logical_not(
                    np.logical_or(model.get(DataModel.ET.LEFT_EYE_X) == self.invalid_value,
                                  model.get(DataModel.ET.LEFT_EYE_Y) == self.invalid_value))
                left_valid_nan = np.logical_not(
                    np.logical_or(np.isnan(model.get(DataModel.ET.LEFT_EYE_X)),
                                  np.isnan(model.get(DataModel.ET.LEFT_EYE_Y))))
                model.raw[model.accessors[DataModel.ET.LEFT_EYE_VALID]] = np.logical_and(left_valid, left_valid_nan)

            if DataModel.ET.RIGHT_EYE_X in model.accessors and DataModel.ET.RIGHT_EYE_Y in model.accessors:
                right_valid = np.logical_not(
                    np.logical_or(model.get(DataModel.ET.RIGHT_EYE_X) == self.invalid_value,
                                  model.get(DataModel.ET.RIGHT_EYE_Y) == self.invalid_value))
                right_valid_nan = np.logical_not(
                    np.logical_or(np.isnan(model.get(DataModel.ET.RIGHT_EYE_X)),
                                  np.isnan(model.get(DataModel.ET.RIGHT_EYE_Y))))
                model.raw[model.accessors[DataModel.ET.RIGHT_EYE_VALID]] = np.logical_and(right_valid, right_valid_nan)

        self.process_events(model)

    def process_events(self, model: DataModel) -> None:
        if DataModel.ET.EVENT_IDX in model.accessors and DataModel.ET.EVENT_TYPE in model.accessors:
            event_start = 0
            event_stop = 0
            previous_event_idx = -1
            previous_event_type = PerceptionToolkit.EyeMovementTypes.EyeMovementTypes.SACCADE
            found_events = []
            for i, idx in enumerate(model.get(DataModel.ET.EVENT_IDX)):
                if previous_event_idx == -1:
                    previous_event_idx = idx
                    previous_event_type = model.get(DataModel.ET.EVENT_TYPE)[i]

                if not previous_event_idx == idx:
                    # finish up old event
                    event_stop = i - 1
                    found_events.append((previous_event_type, event_start, event_stop))
                    # new event starts
                    event_start = i
                    previous_event_type = model.get(DataModel.ET.EVENT_TYPE)[i]
                    previous_event_idx = idx

            # Add the very last event, if it has not been added yet
            if not event_stop == len(model.get(DataModel.ET.EVENT_IDX))-1:
                event_stop = len(model.get(DataModel.ET.EVENT_IDX))-1
                found_events.append((previous_event_type, event_start, event_stop))

            model.events = np.array(found_events)
            model.test_events_consistency()

    def read(self) -> List[DataModel]:
        assert len(self.filename) > 0
        assert (os.path.isfile(self.filename))

        models = []
        raw = pd.read_table(self.filename, sep=self.separator, skiprows=self.skip_header_lines,
                            comment=self.comment_symbol, low_memory=False)

        # check if all specified aliases do occur in the file
        accessors: Dict[DataModel.ET, str] = {}
        for alias in self.aliases:
            if self.aliases[alias] not in raw.columns:
                print("WARNING! Alias", alias, "specified as", self.aliases[alias], "but not found in file.")
            else:
                accessors[DataModel.ET.to_ET(alias)] = self.aliases[alias]
                # this also asserts the string is convertible to ET

        # make sure the data is in float format (we cannot work with any weird arbitrary data in these important fields)
        # TODO one might consider allowing an arbitrary data type for validity until postprocessing is performed
        variables = [DataModel.ET.TIME, DataModel.ET.LEFT_EYE_X, DataModel.ET.LEFT_EYE_Y, DataModel.ET.LEFT_EYE_VALID,
                     DataModel.ET.LEFT_PUPIL_DIAMETER, DataModel.ET.RIGHT_EYE_X, DataModel.ET.RIGHT_EYE_Y,
                     DataModel.ET.RIGHT_EYE_VALID, DataModel.ET.RIGHT_PUPIL_DIAMETER]

        for idx in variables:
            if idx in accessors:
                PersistenceCSV.ensure_float_format(raw, accessors[idx])

        # Split at trial split symbol
        if self.trial_split_symbol:
            trial_start_indices = np.where(raw.isin([self.trial_split_symbol]).any(axis=1))[0]

            trial_stop_indices = np.concatenate((trial_start_indices[1:] - 1, np.array([raw.shape[0]])))
            trial_start_indices += 1  # discard trial split symbol

            if trial_start_indices.size == 0:
                trial_start_indices = np.array([0])
                trial_stop_indices = np.array([raw.shape[0]])

            for i, val in enumerate(trial_start_indices):
                current_model = DataModel()
                pandas_raw = raw.iloc[trial_start_indices[i]:trial_stop_indices[i]].copy()
                # This is very much not elegant, but pandas import features are by now far superior to Tabel's
                current_model.raw = tb.Tabel(pandas_raw)

                current_model.accessors = accessors
                if PersistenceCSV.test_data_assertions(current_model):
                    models.append(current_model)
                else:
                    print("WARNING: Data inconsistent. It will not be loaded.")

        if self.trial_column:
            if self.trial_column not in raw.keys():
                print(
                    "WARNING: Trial column defined as " + self.trial_column + " but not found in data. Aborting load.")
                return []
            unique_trials = raw[self.trial_column].unique()
            for t_id in unique_trials:
                pandas_raw = raw[raw[self.trial_column] == t_id]
                current_model = DataModel()
                current_model.raw = tb.Tabel(pandas_raw)
                current_model.accessors = accessors
                current_model.meta[DataModel.META.TRIAL_NUMBER] = t_id
                if PersistenceCSV.test_data_assertions(current_model):
                    models.append(current_model)
                else:
                    print("WARNING: Data inconsistent. It will not be loaded.")

        if not self.trial_split_symbol and not self.trial_column:
            current_model = DataModel()
            current_model.raw = tb.Tabel(raw)
            current_model.accessors = accessors
            if PersistenceCSV.test_data_assertions(current_model):
                models.append(current_model)
            else:
                print("WARNING: Data inconsistent. It will not be loaded.")

        # apply postprocessing
        [self.post_process(model) for model in models]

        [IPersistencePlugin.report(model) for model in models]
        IPersistencePlugin.report_final(models)

        return models

    @staticmethod
    def test_data_assertions(data: DataModel) -> bool:
        contains_entries = data.raw.shape[0] > 0
        if not contains_entries:
            print("WARNING: Dataset contains no entries.")
            return False
        duration_ok = data.duration() > 0
        """Makes sure all assumptions we have on the data do hold. (e.g., time is always increasing)"""
        is_sorted = lambda a: np.all(a[:-1] <= a[1:])
        timestamps_ok = is_sorted(data.time())
        if not duration_ok:
            print("WARNING: Duration smaller or equal to zero:" + str(data.duration()))
        if not timestamps_ok:
            print("WARNING: Timestamps not sorted!")
        return duration_ok and timestamps_ok

    def write(self, data: Sequence[DataModel]):
        assert len(data) == len(self.target_files)
        for i, d in enumerate(data):
            self.write_single_trial(d, self.target_files[i])

    def write_single_trial(self, data: DataModel, filename: str) -> None:
        assert len(filename) > 0

        # Make a copy of the data and append event data
        event_type = np.zeros(data.raw.shape[0], dtype=np.int)
        event_idx = np.zeros(data.raw.shape[0], dtype=np.int)
        for i in range(0, data.raw.shape[0]):
            event = np.logical_and(data.events[:, 1] <= i, data.events[:, 2] >= i)
            if np.any(event):
                idx = np.where(event)[0][0]
                event_type[i] = data.events[idx, 0]
                event_idx[i] = idx

        tbl = tb.Tabel()
        tbl.append(data.raw)
        tbl["event_type"] = event_type
        tbl["event_idx"] = event_idx

        # this does not save the aliases.
        # tbl.save(filename, 'csv', True)
        with open(filename, 'w') as f:
            self.custom_tabel_writer(f, tbl)

    def custom_tabel_writer(self, f, tabel: tb.Tabel):
        # TODO support timestamp_to_ms_factor and invalid_value for export as well.
        writer = csv.writer(f, delimiter=self.separator)
        writer.writerow(tabel.columns)
        writer.writerows(zip(*tabel.data))

    def preset_tobii(self):
        self.separator = "\t"
        self.timestamp_to_ms_factor = 0.001
        self.invalid_value = -9999
        self.aliases = {"TIME": "Computer timestamp",
                        "LEFT_EYE_X": "Gaze point left X",
                        "LEFT_EYE_Y": "Gaze point left Y",
                        "RIGHT_EYE_X": "Gaze point right X",
                        "RIGHT_EYE_Y": "Gaze point right Y",
                        "LEFT_EYE_VALID": "Validity left",
                        "RIGHT_EYE_VALID": "Validity right",
                        "LEFT_PUPIL_DIAMETER": "Pupil diameter left",
                        "RIGHT_PUPIL_DIAMETER": "Pupil diameter right"}

    def preset_smi(self):
        self.separator = "\t"
        self.skip_header_lines = 4
        self.comment_symbol = "#"
        self.invalid_value = 0
        self.trial_column = "Trial"
        self.trial_split_symbol = "MSG"
        self.timestamp_to_ms_factor = 0.001
        self.aliases = {"TIME": "Time",
                        "LEFT_EYE_X": "L POR X [px]",
                        "LEFT_EYE_Y": "L POR Y [px]",
                        "RIGHT_EYE_X": "R POR X [px]",
                        "RIGHT_EYE_Y": "R POR Y [px]"}

    def preset_smi2(self):
        self.separator = "\t"
        self.skip_header_lines = 4
        self.comment_symbol = "#"
        self.invalid_value = np.nan
        self.trial_column = "Trial"
        self.aliases = {"TIME": "RecordingTime [ms]",
                        "LEFT_EYE_X": "Point of Regard Left X [px]",
                        "LEFT_EYE_Y": "Point of Regard Left Y [px]",
                        "RIGHT_EYE_X": "Point of Regard Right X [px]",
                        "RIGHT_EYE_Y": "Point of Regard Right Y [px]",
                        "LEFT_PUPIL_DIAMETER": "Pupil Diameter Left [mm]",
                        "RIGHT_PUPIL_DIAMETER": "Pupil Diameter Right [mm]"}

    def preset_eyerectoo(self):
        self.separator = "\t"
        self.aliases = {"TIME": "sync.timestamp",
                        "LEFT_EYE_X": "left.gaze.x",
                        "LEFT_EYE_Y": "left.gaze.y",
                        "LEFT_EYE_VALID": "field.gaze.valid",
                        "RIGHT_EYE_X": "right.gaze.x",
                        "RIGHT_EYE_Y": "right.gaze.y",
                        "RIGHT_EYE_VALID": "right.gaze.valid",
                        "LEFT_PUPIL_DIAMETER": "left.pupil.width",
                        "RIGHT_PUPIL_DIAMETER": "right.pupil.width"}
