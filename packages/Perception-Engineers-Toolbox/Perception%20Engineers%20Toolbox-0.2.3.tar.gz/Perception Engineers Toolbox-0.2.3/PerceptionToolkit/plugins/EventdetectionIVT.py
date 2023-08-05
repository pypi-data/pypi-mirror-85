from typing import Sequence, Dict, Any

import numpy as np

from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EventdetectionHelpers import Geometry3D, VelocityCalculator
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from PerceptionToolkit.PluginInterfaces import IEventdetectionPlugin
from PerceptionToolkit.Version import Version


class EventdetectionIVT(IEventdetectionPlugin):
    """I-VT Velocity threshold method

    Following the descriptions in
    Salvucci, D. D., & Goldberg, J. H. (2000, November). Identifying fixations and saccades in eye-tracking protocols.
    In Proceedings of the 2000 symposium on Eye tracking research & applications (pp. 71-78). ACM.

    Disambiguated, extended and made robust by:
    https://www.tobiipro.com/siteassets/tobii-pro/learn-and-support/analyze/how-do-we-classify-eye-movements/tobii-pro-i-vt-fixation-filter.pdf

    Please note that I do not consider data filtering (i.e., gap filling and median filtering) a task of the event
    detection routine. Please apply them separately and beforehand, if you want to (and you probably should).

    Attributes:
        velocity_calculator_window: see `PerceptionToolkit.EventdetectionHelpers.VelocityCalculator`
        velocity_threshold:         see `PerceptionToolkit.EventdetectionHelpers.VelocityCalculator`

        distance_eye_to_stimulus: see `PerceptionToolkit.EventdetectionHelpers.Geometry3D`
        stimulus_pixel_size:      see `PerceptionToolkit.EventdetectionHelpers.Geometry3D`

        merge_adjacent_fixations: see `PerceptionToolkit.PluginInterfaces.IEventdetectionPlugin`
        max_time_between_fixations: see `PerceptionToolkit.PluginInterfaces.IEventdetectionPlugin`
        max_distance_between_fixations: `see PerceptionToolkit.PluginInterfaces.IEventdetectionPlugin`

        discard_short_fixations: [bool] Whether to filter and exclude short fixations as a post processing step
        min_fixation_duration:   [ms] the minimal duration a fixation has to last, in case discard_short_fixations
    """

    def __init__(self):
        super(EventdetectionIVT, self).__init__()
        self.distance_eye_to_stimulus: float = 700  # mm
        self.stimulus_pixel_size: float = 0.15  # mm/px size of a single pixel of the stimulus (assuming square pixels)

        self.velocity_calculator_window: float = 20  # ms
        self.velocity_threshold: float = 30  # °/s

        self.merge_adjacent_fixations: bool = True
        self.max_time_between_fixations: float = 75  # ms
        self.max_distance_between_fixations: float = 0.5  # °

        self.discard_short_fixations: bool = True
        self.min_fixation_duration: float = 60  # ms

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.distance_eye_to_stimulus = parameters.get("distance_eye_to_stimulus", self.distance_eye_to_stimulus)
        self.stimulus_pixel_size = parameters.get("stimulus_pixel_size", self.stimulus_pixel_size)
        self.velocity_calculator_window = parameters.get("velocity_calculator_window", self.velocity_calculator_window)
        self.velocity_threshold = parameters.get("velocity_threshold", self.velocity_threshold)
        self.merge_adjacent_fixations = parameters.get("merge_adjacent_fixations", self.merge_adjacent_fixations)
        self.max_time_between_fixations = parameters.get("max_time_between_fixations", self.max_time_between_fixations)
        self.max_distance_between_fixations = parameters.get("max_distance_between_fixations",
                                                             self.max_distance_between_fixations)
        self.discard_short_fixations = parameters.get("discard_short_fixations", self.discard_short_fixations)
        self.min_fixation_duration = parameters.get("min_fixation_duration", self.min_fixation_duration)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def detect(self, data: DataModel) -> None:
        sampling_frequency: float = data.sampling_frequency()

        if sampling_frequency < 200:
            if sampling_frequency < 50:
                print(
                    "WARN: I-VT is designed to be used with sampling frequencies >200 Hz. Your data is sampled at "
                    "%.1f Hz. This is not the ideal algorithm for your application. Proceeding anyway, assuming you "
                    "know what you are doing. However, for data at <50Hz results are highly questionable." %
                    sampling_frequency)
            else:
                print(
                    "'WARN: I-VT is designed to be used with sampling frequencies >200 Hz. Your data is sampled at "
                    "%.1f Hz. Applying it to data >50Hz is possible but not recommended. Please check the sanity of "
                    "your results carefully." % sampling_frequency)

        t = data.time()
        x = data.x()
        y = data.y()
        v = data.valid()

        # Calculate velocities
        geo: Geometry3D = Geometry3D(eye_distance=self.distance_eye_to_stimulus,
                                     stimulus_pixel_size=self.stimulus_pixel_size)
        vel_calc: VelocityCalculator = VelocityCalculator(self.velocity_calculator_window, geo,
                                                          data.sampling_frequency())

        velocities: Sequence[float] = vel_calc.calculate(t, x, y, v)

        # I-VT classifier
        fixation_started: bool = False
        saccade_started: bool = False
        fixation_start_idx = 0
        saccade_start_idx = 0
        found_events = []

        i = 0
        for i in range(0, len(velocities)):
            if velocities[i] < self.velocity_threshold:
                # Fixation
                if not fixation_started:
                    # finish previous saccade, if any
                    if saccade_started:
                        new_saccade = (EyeMovementTypes.SACCADE, saccade_start_idx, i - 1)
                        assert saccade_start_idx >= 0
                        assert saccade_start_idx < data.raw.shape[0]
                        assert i >= 0
                        assert i < data.raw.shape[0]
                        found_events.append(new_saccade)
                        saccade_started = False
                    fixation_start_idx = i
                    fixation_started = True

            else:
                # Saccade
                if not saccade_started:
                    # finish previous fixation, if any
                    if fixation_started:
                        new_fixation = (EyeMovementTypes.FIXATION, fixation_start_idx, i - 1)
                        found_events.append(new_fixation)
                        fixation_started = False

                    saccade_start_idx = i
                    saccade_started = True

        # Finish up any open events
        if fixation_started:
            new_fixation = (EyeMovementTypes.FIXATION, fixation_start_idx, len(v) - 1)
            found_events.append(new_fixation)

        if saccade_started:
            new_saccade = (EyeMovementTypes.SACCADE, saccade_start_idx, len(v) - 1)
            assert saccade_start_idx >= 0
            assert saccade_start_idx < data.raw.shape[0]
            assert i >= 0
            assert i < data.raw.shape[0]
            found_events.append(new_saccade)

        # merge short nearby fixations
        distance_in_pixels: float = geo.degree2pixels(self.max_distance_between_fixations)
        fixations_before_merge = len(found_events)
        if self.merge_adjacent_fixations:
            IEventdetectionPlugin.merge_adjacent_fixations(found_events, data, self.max_time_between_fixations,
                                                           distance_in_pixels)
        fixations_merged = fixations_before_merge - len(found_events)

        # discard  short  fixations
        fixations_before_discard = len(found_events)
        if self.discard_short_fixations:
            IEventdetectionPlugin.discard_short_fixations(found_events, data, self.min_fixation_duration)
        fixations_discarded = fixations_before_discard - len(found_events)

        data.remove_all_events_of_type([EyeMovementTypes.FIXATION, EyeMovementTypes.SACCADE])
        if data.events.size > 0:
            data.events = np.append(data.events, np.array(found_events), axis=0)
        else:
            data.events = np.array(found_events)

        data.test_events_consistency()
        print("Found %i Fixations and %i Saccades (%i merged, %i discarded)." % (
        data.fixations().shape[0], data.saccades().shape[0], fixations_merged, fixations_discarded))
