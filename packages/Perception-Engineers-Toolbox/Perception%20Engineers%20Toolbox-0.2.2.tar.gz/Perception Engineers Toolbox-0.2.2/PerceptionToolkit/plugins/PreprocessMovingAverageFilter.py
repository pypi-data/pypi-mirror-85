from PerceptionToolkit.PluginInterfaces import IPreprocessingPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
import numpy as np
from typing import Dict, Any, Sequence


class PreprocessMovingAverageFilter(IPreprocessingPlugin):
    def __init__(self):
        super(PreprocessMovingAverageFilter, self).__init__()
        self.time_window = 22  # ms (same as Tobii)

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.time_window = parameters.get("time_window", self.time_window)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def process(self, data: DataModel) -> None:
        # for the sake of run-time benefits we assume a fixed framerate.
        fps: float = data.sampling_frequency()
        window_width: int = int(self.time_window / 1000.0 * fps + 1)
        if window_width % 2 == 0:
            window_width += 1

        variables: Sequence[DataModel.ET] = [DataModel.ET.LEFT_EYE_X, DataModel.ET.LEFT_EYE_Y, DataModel.ET.LEFT_PUPIL_DIAMETER,
                     DataModel.ET.RIGHT_EYE_X, DataModel.ET.RIGHT_EYE_Y, DataModel.ET.RIGHT_PUPIL_DIAMETER]
        for variable in variables:
            if variable in data.accessors and data.accessors[variable]:
                # We cannot smooth data points that are not within the filter window with this approach.
                # Therefore, they are left untouched. Same for points where the filter contains nans
                data.raw[:, data.accessors[variable]] = PreprocessMovingAverageFilter.convolve_mean(
                    data.raw[:, data.accessors[variable]], window_width)
        print("Moving average filter (kernel width", self.time_window, "ms =", window_width, "samples) applied.")

    @staticmethod
    def convolve_mean(a, n):
        ret = np.convolve(a, np.ones(n) / n, mode='valid')
        a_excerpt = a[int(n / 2):-int(n / 2)]
        ret[np.isnan(ret)] = a_excerpt[np.isnan(ret)]
        return np.append(np.append(a[0:int(n / 2)], ret, axis=0), a[-int(n / 2):], axis=0)
