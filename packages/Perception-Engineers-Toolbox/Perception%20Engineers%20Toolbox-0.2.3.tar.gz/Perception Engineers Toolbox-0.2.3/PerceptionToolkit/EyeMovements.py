from PerceptionToolkit.DataModel import DataModel
import numpy as np
import math
from PerceptionToolkit.EventdetectionHelpers import VelocityCalculatorPixels


class Fixation:
    """Represents a fixation and calculates its characteristic values."""

    def __init__(self, model: DataModel, start_idx: int, end_idx: int):
        assert start_idx <= end_idx
        self.startTime = model.time()[start_idx] - model.ms_per_frame() / 2
        self.endTime = model.time()[end_idx] + model.ms_per_frame() / 2
        assert self.startTime <= self.endTime
        self.duration = self.endTime - self.startTime
        assert self.duration >= 0
        self.centroid = (np.mean(model.x()[start_idx:end_idx + 1]), np.mean(model.y()[start_idx:end_idx + 1]))
        self.std = (np.std(model.x()[start_idx:end_idx + 1]) + np.std(model.y()[start_idx:end_idx + 1])) / 2
        self.x_range = max(model.x()[start_idx:end_idx + 1]) - min(model.x()[start_idx:end_idx + 1])
        self.y_range = max(model.y()[start_idx:end_idx + 1]) - min(model.y()[start_idx:end_idx + 1])


class Saccade:
    """Represents a saccade and calculates its characteristic values.

    TODO we should probably copy the sample data here and calculate measures only on requirement via functions instead
    of via constructor. Or provide the raw data each time we ask for features.
    (Or require supplying the DataModel and only saving the indices when querying a property)
    That would be beneficial for run-time in most cases.
    """

    def __init__(self, model: DataModel, start_idx: int, end_idx: int):
        if end_idx < start_idx:  # for small sampling rates there might not be a single sample assigned to this
            # fixation. This is signalled by its end index being smaller than its start index.
            end_idx = start_idx
            self.startTime = model.time()[start_idx]
            self.endTime = self.startTime
            self.duration = np.nan  # we cannot tell at all and therefore not even assign a fraction of a sampling
            # duration. However, (Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 458):
            # no saccades below 21ms. I did not implement this though, as it might lead to unexpected effects.
        else:
            self.startTime = model.time()[start_idx] - model.ms_per_frame() / 2
            self.endTime = model.time()[end_idx] + model.ms_per_frame() / 2
            self.duration = self.endTime - self.startTime

        assert self.startTime <= self.endTime

        if not start_idx >= end_idx:

            x = model.x()[start_idx:end_idx+1]
            y = model.y()[start_idx:end_idx+1]
            # calculated by piecewise segment lengths between samples
            self.amplitude = np.sum(np.sqrt(np.power(np.diff(x), 2) + np.power(np.diff(y), 2)))
            self.direction = math.degrees(math.atan2(y[0] - y[-1], x[0] - x[-1]))

            def point_line_distance(p3, p1, p2):
                np.abs(np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1))

            p = np.vstack((x, y))
            sample_straight_distances = np.apply_along_axis(point_line_distance, 0, p, p1=p[:, 0], p2=p[:, -1])
            if not all(v is None for v in sample_straight_distances):
                self.curvature = np.max(sample_straight_distances)
            else:
                self.curvature = np.nan

            if end_idx - start_idx >= 2:  # That's what's require to calculate velocities
                # This value of 20 ms is kind of arbitrary. That's even why we need the guard in case the sampling
                # rate is not sufficient. However, it is probably better to have some kind of temporal filter to
                # reduce some noise.
                velocities = VelocityCalculatorPixels(max(20., model.ms_per_frame()),
                                                      model.sampling_frequency()).calculate(
                    model.time()[start_idx:end_idx+1], model.x()[start_idx:end_idx+1],
                    model.y()[start_idx:end_idx+1],
                    model.valid()[start_idx:end_idx+1])

                if (not all(v is None for v in velocities) or not all(v is np.NaN for v in velocities)) and len(velocities) > 0:
                    self.average_velocity = np.nanmean(velocities)
                    self.peak_velocity = np.nanmax(velocities)
                    self.time_to_peak = np.argmax(velocities) * model.ms_per_frame()
                else:
                    self.average_velocity = np.nan
                    self.peak_velocity = np.nan
                    self.time_to_peak = np.nan
            else:
                self.average_velocity = np.nan
                self.peak_velocity = np.nan
                self.time_to_peak = np.nan
        else:
            # TODO use the previous eye movements end and the following eye movements start as a support structure, as
            # no other data is available.
            # x = model.x().iloc[end_idx:start_idx]
            # y = model.y().iloc[end_idx:start_idx]
            # self.amplitude = np.sum(np.sqrt(np.power(np.diff(x), 2) + np.power(np.diff(y), 2)))
            # self.direction = math.degrees(math.atan2(y.iloc[-1] - y.iloc[0], x.iloc[-1] - x.iloc[0]))
            self.amplitude = np.nan
            self.direction = np.nan
            self.average_velocity = np.nan
            self.peak_velocity = np.nan
            self.time_to_peak = np.nan


class Microsaccade:
    """Represents a microsaccade and calculates its characteristic values."""

    def __init__(self, model: DataModel, start_idx: int, end_idx: int):
        if end_idx < start_idx:  # for small sampling rates there might not be a single sample assigned to this
            # microsaccade. This is signalled by its end index being smaller than its start index.
            self.startTime = model.time()[start_idx]
            self.endTime = self.startTime
            self.duration = np.nan  # we cannot tell at all and therefore not even assign a fraction of a sampling
            # duration. However, (Eye Tracking: A comprehensive guide to methods, paradigms, and measures. Page 458):
            # no saccades below 21ms. I did not implement this though, as it might lead to unexpected effects.
        else:
            self.startTime = model.time()[start_idx] - model.ms_per_frame() / 2
            self.endTime = model.time()[end_idx] + model.ms_per_frame() / 2
            self.duration = self.endTime - self.startTime

        assert self.startTime <= self.endTime
