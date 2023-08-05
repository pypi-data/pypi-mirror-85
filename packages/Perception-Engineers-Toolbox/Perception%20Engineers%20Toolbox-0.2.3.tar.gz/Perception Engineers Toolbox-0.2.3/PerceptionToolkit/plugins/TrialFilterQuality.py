from PerceptionToolkit.PluginInterfaces import ITrialFilterPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from typing import List, Dict, Any
import numpy as np
from itertools import compress

class TrialFilterQuality(ITrialFilterPlugin):
    """Filters trials by quality

    Calculates the tracking ratio as
    tracking ratio = number of valid samples / number of total samples

    Attributes:
        min_tracking_ratio: the minimal tracking ratio that is still considered good. Based on the setup and device used
            this value usually varies between 85% - 95% (some blinks will always be there). With 85% you are probably at
            the threshold where event detection might begin to produce weird results.
    """

    def __init__(self):
        super(TrialFilterQuality, self).__init__()
        self.min_tracking_ratio = 0.85

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.min_tracking_ratio = parameters.get("min_tracking_ratio", self.min_tracking_ratio)
        assert 0 <= self.min_tracking_ratio <= 1.0

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def filter(self, data: List[DataModel]) -> List[DataModel]:
        tracking_ratios: List[float] = [self.tracking_ratio(d) for d in data]
        quality_ok: List[bool] = [r >= self.min_tracking_ratio for r in tracking_ratios]
        print("Removed " + str(len(data)-np.sum(quality_ok)) + "/" + str(len(data)) + " trials due to low quality.")
        return list(compress(data, quality_ok))

    def tracking_ratio(self, data: DataModel) -> float:
        v = data.valid()
        return np.sum(v) / len(v)
