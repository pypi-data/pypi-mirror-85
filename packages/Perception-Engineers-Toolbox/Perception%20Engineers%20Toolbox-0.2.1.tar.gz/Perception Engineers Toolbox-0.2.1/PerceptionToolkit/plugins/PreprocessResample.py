from PerceptionToolkit.PluginInterfaces import IPreprocessingPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
import numpy as np
from typing import Dict, Sequence, Any
import tabel as tb


class PreprocessResample(IPreprocessingPlugin):
    """
    UNTESTED!

    Resamples at a given sampling rate.
    Useful for downsampling data or for resampling at constant time intervals

    Attributes:
        target_sampling_rate: samples per second that should be targeted.
    """
    def __init__(self):
        super(PreprocessResample, self).__init__()
        self.target_sampling_rate = 22  # ms (same as Tobii uses)

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.target_sampling_rate = parameters.get("target_sampling_rate", self.target_sampling_rate)

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 2)

    def interpolate(self,  data: DataModel, variable):
        # We need to allocate a new table
        number_of_samples = int((data.time()[-1] - data.time()[0]) / 1000.0 * self.target_sampling_rate)
        raw = tb.Tabel()

        for var in variable:
            if var in data.accessors:
                target_intervals = np.linspace(data.time()[0], data.time()[-1], number_of_samples)
                raw[data.accessors[var]] = np.interp(target_intervals, data.time(), data.get(var))

        data.raw = raw

    def process(self, data: DataModel) -> None:
        original_sampling_rate = data.sampling_frequency()
        original_number_of_samples = data.sample_count()
        if data.events and data.events.shape[0] > 0:
            print("WARNING: Resampling with detected events. Event6s will not be resampled but deleted.")
            data.events = np.empty((1, 3), dtype=np.int)

        self.interpolate(data, [DataModel.ET.TIME,
                                DataModel.ET.RIGHT_EYE_X, DataModel.ET.RIGHT_EYE_Y, DataModel.ET.RIGHT_PUPIL_DIAMETER, DataModel.ET.RIGHT_EYE_VALID,
                                DataModel.ET.LEFT_EYE_X, DataModel.ET.LEFT_EYE_Y, DataModel.ET.LEFT_PUPIL_DIAMETER, DataModel.ET.LEFT_EYE_VALID])
        print("Resampled from %.1fHz to %.1fHz (%i to %i samples)." % (original_sampling_rate, data.sampling_frequency(), original_number_of_samples, data.sample_count()))