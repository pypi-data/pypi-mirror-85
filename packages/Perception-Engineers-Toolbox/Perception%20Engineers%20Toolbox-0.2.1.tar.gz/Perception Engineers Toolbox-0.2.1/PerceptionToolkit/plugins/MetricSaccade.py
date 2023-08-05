from PerceptionToolkit.PluginInterfaces import IMetricPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovements import Saccade
from PerceptionToolkit.Version import Version
import numpy as np
from typing import Dict, Any


class MetricSaccade(IMetricPlugin):
    """Calculates a set of metrics that are characteristic to fixation eye movements and averages them over the trial
    duration. """

    def __init__(self):
        super(MetricSaccade, self).__init__()

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        pass

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def calculate(self, data: DataModel) -> None:
        saccades = data.saccades()

        if saccades.shape[0] == 0:
            # exit gracefully
            print("WARNING: No saccades in data. Did you calculate them?")
            return

        assert saccades.shape[0] > 0

        aggregate_property = lambda attribute: lambda x: getattr(Saccade(data, x[1], x[2]), attribute)

        # I am using the new edition of the book, as the library made my old version disappear...
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 551
        data.metrics["number_of_saccades"] = saccades.shape[0]
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 458
        data.metrics["average_saccade_duration"] = np.nanmean(
            np.apply_along_axis(aggregate_property("duration"), 1, saccades))  # ms
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 552
        data.metrics["saccade_rate"] = saccades.shape[0] / data.duration() * 1000  # 1/s
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 448
        average_saccade_amplitude = np.nanmean(np.apply_along_axis(aggregate_property("amplitude"), 1, saccades))
        data.metrics["average_saccade_amplitude"] = average_saccade_amplitude  # °

        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 439ff
        #data.metrics["saccade_direction"] = np.nanmean(np.apply_along_axis(aggregate_property("direction"), 1, saccades))  # °

        # HV-ratio Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 442
        hv_ratio = 0
        for i in range(0, saccades.shape[0]):
            x_dir = data.x()[saccades[i, 2]] - data.x()[saccades[i, 1]]
            y_dir = data.y()[saccades[i, 2]] - data.y()[saccades[i, 1]]
            if not y_dir == 0:
                hv_ratio += abs(x_dir / y_dir)
        hv_ratio = hv_ratio / saccades.shape[0]
        data.metrics["hv_ratio"] = hv_ratio

        # Skewness Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 452
        # This definition only works for angular values! Not when they are based on pixels :-(
        #skewness_norm_factor = math.sqrt(6/saccades.shape[0])
        #skewness = np.nanmean(np.power(np.apply_along_axis(aggregate_property("amplitude"), 1, saccades)-average_saccade_amplitude, 3)) / math.pow(skewness_norm_factor, 3)
        #data.metrics["saccade_amplitude_skewness"] = skewness

        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 463
        data.metrics["average_saccade_velocity"] = np.nanmean(
            np.apply_along_axis(aggregate_property("average_velocity"), 1, saccades))  # ms
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 465
        data.metrics["average_peak_saccade_velocity"] = np.nanmean(
            np.apply_along_axis(aggregate_property("peak_velocity"), 1, saccades))  # px / s
        # Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 465
        data.metrics["average_time_to_saccade_peak"] = np.nanmean(
            np.apply_along_axis(aggregate_property("time_to_peak"), 1, saccades))  # ms

        print("number_of_saccades: %.0f" % data.metrics["number_of_saccades"])
        print("average_saccade_duration: %.2f ms" % data.metrics["average_saccade_duration"])
        print("saccade_rate: %.2f /s" % data.metrics["saccade_rate"])
        print("hv_ratio: %.2f" % data.metrics["hv_ratio"])
        print("average_saccade_amplitude: %.1f px" % data.metrics["average_saccade_amplitude"])
        print("average_saccade_velocity: %.1f px/s" % data.metrics["average_saccade_velocity"])
        print("average_peak_saccade_velocity: %.1f px/s" % data.metrics["average_peak_saccade_velocity"])
        print("average_time_to_saccade_peak: %.2f ms" % data.metrics["average_time_to_saccade_peak"])
