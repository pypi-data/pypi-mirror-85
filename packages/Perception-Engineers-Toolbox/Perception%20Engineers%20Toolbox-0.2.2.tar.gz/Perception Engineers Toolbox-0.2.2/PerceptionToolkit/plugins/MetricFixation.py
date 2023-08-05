from PerceptionToolkit.PluginInterfaces import IMetricPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovements import Fixation
from PerceptionToolkit.Version import Version
from scipy.spatial import ConvexHull
import numpy as np
from typing import Dict, Any


#    @staticmethod
#    def across_fixation_convex_hull(data: DataModel) -> float:
#        area: float = 0.0
#        samples = []
#        fixations = data.fixations()
#        for f in range(0, fixations.shape[0]):
#            samples.append(Fixation(data, fixations[f, 1], fixations[f, 2]).centroid)
#        try:
#            hull = ConvexHull(np.array(samples))
#            return hull.area
#        except:
#            # For some weird protocols, fixations might just contain a single or two sample. No hull calculation is
#            # possible then.
#            # This is also the case, if there are enough points but they are coincident.
#            return 0

class MetricFixation(IMetricPlugin):
    """Calculates a set of metrics that are characteristic to fixation eye movements and averages them over the trial
    duration. """

    def __init__(self):
        super(MetricFixation, self).__init__()

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        pass

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def calculate(self, data: DataModel) -> None:
        fixations = data.fixations()
        assert fixations.shape[0] > 0

        aggregate_property = lambda attribute: lambda x: getattr(Fixation(data, x[1], x[2]), attribute)

        # I am using the new edition of the book, as the library made my old version disappear...
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 526
        data.metrics["average_fixation_duration"] = np.mean(
            np.apply_along_axis(aggregate_property("duration"), 1, fixations))  # ms
        data.metrics["standard_deviation_fixation_duration"] = np.std(
            np.apply_along_axis(aggregate_property("duration"), 1, fixations))  # ms
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 560
        data.metrics["number_of_fixations"] = fixations.shape[0]
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 565
        data.metrics["fixation_rate"] = fixations.shape[0] / data.duration() * 1000  # 1/s
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures (14.1)
        data.metrics["within_fixations_std"] = np.mean(np.apply_along_axis(aggregate_property("std"), 1, fixations))
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures (14.3)
        data.metrics["within_fixations_x_range"] = np.mean(
            np.apply_along_axis(aggregate_property("x_range"), 1, fixations))
        data.metrics["within_fixations_y_range"] = np.mean(
            np.apply_along_axis(aggregate_property("y_range"), 1, fixations))

        # this is more of a scanpath measure than a fixation property
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 506
        # data.metrics["across_fixation_convex_hull"] = PositionDispersion.across_fixation_convex_hull(data)

        print("number_of_fixations: %.0f" % data.metrics["number_of_fixations"])
        print("average_fixation_duration: %.2f ms" % data.metrics["average_fixation_duration"])
        print("standard_deviation_fixation_duration: %.2f ms" % data.metrics["standard_deviation_fixation_duration"])
        print("fixation_rate: %.2f /s" % data.metrics["fixation_rate"])
        print("within_fixations_std: %.2f px" % data.metrics["within_fixations_std"])
        print("within_fixations_x_range: %.2f px" % data.metrics["within_fixations_x_range"])
        print("within_fixations_y_range: %.2f px" % data.metrics["within_fixations_y_range"])
