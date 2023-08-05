from PerceptionToolkit.PluginInterfaces import IEventdetectionPlugin
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from PerceptionToolkit.Version import Version
import math
from typing import Dict, Any


class EventdetectionIDT(IEventdetectionPlugin):
    """I-DT identification by dispersion threshold

    Implements the I-DT as in SMI BeGaze for low speed fixation detection
    described in the manual available at (Dec 2019)
    http://www.humre.vu.lt/files/doc/Instrukcijos/SMI/BeGaze2.pdf

    Following the descriptions in
    Salvucci, D. D., & Goldberg, J. H. (2000, November). Identifying fixations and saccades in eye-tracking protocols.
    In Proceedings of the 2000 symposium on Eye tracking research & applications (pp. 71-78). ACM.

    With the choice to define the dispersion, following Salvucci and Goldberg, as
    Dispersion = max(x)-min(x) + max(y) - min(y)

    Furthermore, I-DT mentions a fixation merging step that is not further specified. We utilize the definition from
    I-VT for this purpose.

    Attributes: max_fixation_dispersion: [pixels] dispersion threshold. If the dispersion is smaller, we decide to be
    within a fixation, otherwise outside. min_fixation_duration:   [ms] minimal duration that a fixation needs to
    last in order to be included

        merge_adjacent_fixations: see IEventdetectionPlugin
        max_time_between_fixations: see IEventdetectionPlugin
        max_distance_between_fixations: see IEventdetectionPlugin

    """

    def __init__(self):
        super(EventdetectionIDT, self).__init__()
        self.max_fixation_dispersion = 100  # pixels
        self.min_fixation_duration: float = 60  # ms

        self.merge_adjacent_fixations = True
        self.max_time_between_fixations = 75  # ms
        self.max_distance_between_fixations = 100  # same unit as dispersion

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.max_fixation_dispersion = parameters.get("max_fixation_dispersion", self.max_fixation_dispersion)
        self.min_fixation_duration = parameters.get("min_fixation_duration", self.min_fixation_duration)
        self.merge_adjacent_fixations = parameters.get("merge_adjacent_fixations", self.merge_adjacent_fixations)
        self.max_time_between_fixations = parameters.get("max_time_between_fixations", self.max_time_between_fixations)
        self.max_distance_between_fixations = parameters.get("max_distance_between_fixations",
                                                             self.max_distance_between_fixations)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    @staticmethod
    def dispersion_salvucci_goldberg(x: np.array, y: np.array) -> float:
        """Dispersion as defined by Salvucci and Goldberg.

        An actual unique definition is not available, some use the standard deviation or similar measures. We define it
        as
        Dispersion = max(x)-min(x) + max(y) - min(y)

        Note that we do not use the factor 0.5 as in
        "Eye Tracking A comprehensive Guide to Methods And Measures" (Holmqvist & Nyström, 2011)
        as SMI BeGaze does neither, judging from the documentation.
        """

        assert x.size > 0
        assert x.size == y.size
        return (x.max() - x.min()) + (y.max() - y.min())

    def detect(self, data: DataModel) -> None:
        sampling_frequency: float = data.sampling_frequency()

        if sampling_frequency >= 200:
            print(
                "WARN: I-DT is designed to be used with sampling frequencies <200Hz. Your data is sampled at %.1f Hz. "
                "This might not be the ideal algorithm for your application. Proceeding anyway, assuming you know "
                "what you are doing." % sampling_frequency)

            # Sliding window with minimum fixation duration
        sliding_window_position: int = 0
        sliding_window_base_width: int = int(math.ceil(self.min_fixation_duration / (1000.0 / sampling_frequency)))
        assert (sliding_window_base_width > 0)

        within_fixation: bool = False
        sliding_window_width: int = sliding_window_base_width

        found_events = []

        x = data.x()
        y = data.y()
        v = data.valid()

        while sliding_window_position < data.sample_count():
            # The case that the window approaches the end of the trial is not explicitly handled in the literature.
            # This implementation shortens the window to the length of the trial. Cutting off would also be possible.
            sliding_window_stop: int = min(sliding_window_position + sliding_window_width, data.sample_count() - 1)

            window_x = x[sliding_window_position:(sliding_window_stop + 1)]
            window_y = y[sliding_window_position:(sliding_window_stop + 1)]
            window_v = v[sliding_window_position:(sliding_window_stop + 1)]

            if (EventdetectionIDT.dispersion_salvucci_goldberg(window_x, window_y) > self.max_fixation_dispersion) or \
                    np.any(window_v <= 0.5):
                # Terminate previous fixation
                if within_fixation:
                    new_fixation = (EyeMovementTypes.FIXATION, sliding_window_position,
                                    sliding_window_stop)
                    found_events.append(new_fixation)
                    within_fixation = False
                    sliding_window_position = sliding_window_stop + 1
                    sliding_window_width = sliding_window_base_width
                else:
                    sliding_window_position += 1

            else:
                # Fixation starts or continues
                within_fixation = True
                sliding_window_width += 1

                # end of trial reached. Finish up open events.
                if sliding_window_position + sliding_window_width >= data.sample_count() - 1:
                    new_fixation = (EyeMovementTypes.FIXATION, sliding_window_position,
                                    sliding_window_stop)
                    found_events.append(new_fixation)

                    break

        fixations_before_merge = len(found_events)
        if self.merge_adjacent_fixations:
            IEventdetectionPlugin.merge_adjacent_fixations(found_events, data, self.max_time_between_fixations,
                                                           self.max_distance_between_fixations)
        fixations_merged = fixations_before_merge - len(found_events)

        # For I-DT we do not have to check a minimum fixation duration, as the sliding window assures the time
        # constraint already

        data.remove_all_events_of_type([EyeMovementTypes.FIXATION, EyeMovementTypes.SACCADE])
        if data.events.size > 0:
            data.events = np.append(data.events, np.array(found_events), axis=0)
        else:
            data.events = np.array(found_events)

        # now insert saccades between the fixations
        EventdetectionIDT.insert_saccades(data)
        data.test_events_consistency()
        print("Found %i Fixations and %i Saccades (%i merged)." % (data.fixations().shape[0], data.saccades().shape[0], fixations_merged))

    @staticmethod
    def insert_saccades(data: DataModel):
        saccades = []
        fixations = data.fixations()
        for i in range(0, fixations.shape[0] - 1):
            new_saccade = (EyeMovementTypes.SACCADE, fixations[i, 2] + 1, fixations[i + 1, 1] - 1)
            # We can actually have the end of a saccade before its start, in case there is not a single sample that
            # can be assigned to the saccade (e.g., for 30 Hz Trackers) assert fixations[i, 2]+1 >= fixations[i+1, 1]-1
            saccades.append(new_saccade)
        if not len(saccades) == 0:
            data.events = np.vstack([data.events, np.array(saccades)])
