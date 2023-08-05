from PerceptionToolkit.PluginInterfaces import IPreprocessingPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
import numpy as np
from typing import Dict, Sequence, Any


class PreprocessGapFill(IPreprocessingPlugin):
    """
    Allows to fill short gaps in the data signal via linear interpolation from neighboring valid samples.

    Interpolated samples will be declared valid samples.

    Attributes:
        max_gap_length: The maximum duration [ms] that the gap may extend over so that it is still considered for
            filling. Long gaps in the data should not be filled, as the linear interpolation approach is unlikely to be
            adequate for longer tracking losses.
    """
    def __init__(self):
        super(PreprocessGapFill, self).__init__()
        self.max_gap_length = 22  # ms (same as Tobii uses)

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        # limits the maximum length of a gap that should be filled-in, i.e. the
        # maximum duration a gap can be without being treated as a ‘legitimate’ gap
        # such as a blink or data loss caused by the participant looking away or
        # obscuring the eye trackerFilled
        self.max_gap_length = parameters.get("max_gap_length", self.max_gap_length)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def check_gap_length(self, t1: float, t2: float) -> bool:
        return t2 - t1 <= self.max_gap_length

    @staticmethod
    def linear_interpolation(x0: float, y0: float, xN: float, yN: float, x: float) -> float:
        return y0 + (x - x0) * ((yN - y0) / (xN - x0))

    @staticmethod
    def interpolate_gap_variable(data: DataModel, validity: DataModel.ET, variable: DataModel.ET, start_of_gap: int,
                                 end_of_gap: int) -> None:
        t0 = data.raw[start_of_gap - 1, data.accessors[DataModel.ET.TIME]]
        x0 = data.raw[start_of_gap - 1, data.accessors[variable]]
        tN = data.raw[end_of_gap + 1, data.accessors[DataModel.ET.TIME]]
        xN = data.raw[end_of_gap + 1, data.accessors[variable]]
        t = data.raw[start_of_gap:end_of_gap, data.accessors[DataModel.ET.TIME]]
        data.raw[start_of_gap:end_of_gap, data.accessors[variable]] = PreprocessGapFill.linear_interpolation(t0, x0,
                                                                                                             tN, xN,
                                                                                                             t)
        data.raw[start_of_gap:end_of_gap, data.accessors[validity]] = 1.0  # Declares interpolated data as valid

    @staticmethod
    def interpolate_gap(data: DataModel, validity: DataModel.ET, start_of_gap: int, end_of_gap: int,
                        variables: Sequence[DataModel.ET]) -> None:
        for variable in variables:
            if variable in data.accessors and data.accessors[variable]:
                PreprocessGapFill.interpolate_gap_variable(data, validity, variable, start_of_gap, end_of_gap)

    def interpolate(self, data: DataModel, validity_col: DataModel.ET, variables: Sequence[DataModel.ET]):
        validity = data.get(validity_col)
        time = data.time()
        last_valid_sample_idx: int = -1
        gaps_filled: int = 0
        samples_interpolated: int = 0

        it = np.nditer(validity, flags=['f_index'])
        while not it.finished:
            valid = it[0]
            idx = it.index
            it.iternext()
            if not valid:  # actually either 0 or 1, but this enables it to work with a confidence measure as well
                continue
            else:
                # are we finishing a gap (and it is not at the very beginning of the recording)
                if not (last_valid_sample_idx == idx - 1) and not (last_valid_sample_idx == -1):
                    if self.check_gap_length((time[last_valid_sample_idx] + time[last_valid_sample_idx + 1]) / 2,
                                             (time[idx - 1] + time[idx]) / 2):
                        PreprocessGapFill.interpolate_gap(data, validity_col, last_valid_sample_idx + 1, idx - 1,
                                                          variables)
                        gaps_filled += 1
                        samples_interpolated += idx - last_valid_sample_idx - 1

                last_valid_sample_idx = idx

        eye_string = "[left eye]"
        if validity_col == DataModel.ET.RIGHT_EYE_VALID:
            eye_string = "[right eye]"

        print("Filled %i gaps (%i = %.2f%% of total samples interpolated) %s." %
              (gaps_filled, samples_interpolated, samples_interpolated / validity.size * 100, eye_string)
              )

    def process(self, data: DataModel) -> None:
        if DataModel.ET.RIGHT_EYE_VALID in data.accessors:
            self.interpolate(data, DataModel.ET.RIGHT_EYE_VALID,
                             [DataModel.ET.RIGHT_EYE_X, DataModel.ET.RIGHT_EYE_Y, DataModel.ET.RIGHT_PUPIL_DIAMETER])

        if DataModel.ET.LEFT_EYE_VALID in data.accessors:
            self.interpolate(data, DataModel.ET.LEFT_EYE_VALID,
                             [DataModel.ET.LEFT_EYE_X, DataModel.ET.LEFT_EYE_Y, DataModel.ET.LEFT_PUPIL_DIAMETER])
