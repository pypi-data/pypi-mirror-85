from PerceptionToolkit.PluginInterfaces import ITrialFilterPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from typing import List, Dict, Any
import numpy as np
from itertools import compress


class TrialFilterProperty(ITrialFilterPlugin):
    """Filters trials by properties of the trial

    Attributes:
        minimum_sampling_frequency: the sampling rate that is expected. Please note that there might be some floating
            point inaccuracies that should be considered when choosing this threshold (i.e., choose it slightly lower
            than the expected rate).
        minimum_duration: The minimal trial duration to expect [ms].
    """

    def __init__(self):
        super(TrialFilterProperty, self).__init__()
        self.minimum_sampling_frequency = -1
        self.minimum_duration = -1

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.minimum_sampling_frequency = parameters.get("minimum_sampling_frequency", self.minimum_sampling_frequency)
        self.minimum_duration = parameters.get("minimum_duration", self.minimum_duration)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def filter(self, data: List[DataModel]) -> List[DataModel]:
        sampling_frequency_ok: List[bool] = [d.sampling_frequency() >= self.minimum_sampling_frequency for d in data]
        duration_ok: List[bool] = [d.duration() >= self.minimum_duration for d in data]
        trial_ok = np.logical_and(sampling_frequency_ok, duration_ok)
        print("Removed " + str(len(data) - np.sum(trial_ok)) + "/" + str(len(data)) + " trials due to trial properties not matching.")
        return list(compress(data, trial_ok))
