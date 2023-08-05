from PerceptionToolkit.PluginInterfaces import IPreprocessingPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from scipy.signal import medfilt
from typing import Dict, Any, Sequence


class PreprocessMedianFilter(IPreprocessingPlugin):
    def __init__(self):
        super(PreprocessMedianFilter, self).__init__()
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

        variables: Sequence[DataModel.ET] = [DataModel.ET.LEFT_EYE_X, DataModel.ET.LEFT_EYE_Y,
                                             DataModel.ET.LEFT_PUPIL_DIAMETER, DataModel.ET.RIGHT_EYE_X,
                                             DataModel.ET.RIGHT_EYE_Y, DataModel.ET.RIGHT_PUPIL_DIAMETER]
        for variable in variables:
            if variable in data.accessors and data.accessors[variable]:
                data.raw[:, data.accessors[variable]] = medfilt(data.raw[:, data.accessors[variable]],
                                                                kernel_size=window_width)

        print("Median filter (kernel width", self.time_window, "ms =", window_width, "samples) applied.")
