from PerceptionToolkit.PluginInterfaces import IEventdetectionPlugin
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from typing import Sequence, List, Tuple, Any, Dict
from PerceptionToolkit.EyeMovements import Microsaccade
from PerceptionToolkit.Version import Version


class EventdetectionEngelbert(IEventdetectionPlugin):
    """Microsaccade detection after Engelbert and Kliegl.

    Following the descriptions in Engbert, Ralf, and Reinhold Kliegl. "Microsaccades uncover the orientation of
    covert attention." Vision research 43.9 (2003): 1035-1045. And the code available at
    http://read.psych.uni-potsdam.de/index.php?option=com_content&view=article&id=140:engbert-et-al-2015-microsaccade
    -toolbox-for-r&catid=26:publications&Itemid=34


    Attributes:
        lambda_weight: the lambda factor for scaling of the microsaccade detection threshold
        min_duration: the minimum duration of a microsaccade
        require_binocular: enforce that a microsaccade is a binocular event that is required to occur simultaneously
        in both eyes.
    """

    def __init__(self):
        super(EventdetectionEngelbert, self).__init__()
        self.lambda_weight = 6
        self.min_duration = 6  # ms (Nyström, Marcus, et al. "Why have microsaccades become larger? Investigating eye
        # deformations and detection algorithms." Vision research 118 (2016): 17-24.)
        self.require_binocular = True

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.lambda_weight = parameters.get("lambda_weight", self.lambda_weight)
        self.min_duration = parameters.get("min_duration", self.min_duration)
        self.require_binocular = parameters.get("require_binocular", self.require_binocular)

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 1)

    def detect_microsaccades(self, t: np.array, x: np.array, y: np.array, v: np.array) -> List[Tuple[EyeMovementTypes, int, int]]:
        # Calculate velocities
        velocities: np.array = VelocityCalculatorEngelbert.calculate(t, x, y, v)

        medx = np.median(velocities[:, 0])
        msdx = np.sqrt(np.median(np.power(velocities[:, 0] - medx, 2)))
        medy = np.median(velocities[:, 1])
        msdy = np.sqrt(np.median(np.power(velocities[:, 1] - medy, 2)))

        if msdx < 1e-10:
            msdx = np.sqrt(np.nanmean(np.power(velocities[:, 0], 2)) - np.power(np.nanmean(velocities[:, 0]), 2))
        if msdy < 1e-10:
            msdy = np.sqrt(np.nanmean(np.power(velocities[:, 1], 2)) - np.power(np.nanmean(velocities[:, 1]), 2))

        radius_x = self.lambda_weight * msdx
        radius_y = self.lambda_weight * msdy

        test_criterion = np.power((velocities[:, 0] / radius_x), 2) + np.power((velocities[:, 1] / radius_y), 2)
        test_criterion = test_criterion > 1

        # I-VT classifier on the microsaccade criterion
        # Here is where we leave the reference implementation and stick to our I-VT code instead. It should however do
        # the same thing.
        microsaccade_started: bool = False
        microsaccade_start_idx = 0
        found_events = []

        for i in range(0, len(velocities)):
            if test_criterion[i]:
                # microsaccade
                if not microsaccade_started:
                    microsaccade_start_idx = i
                    microsaccade_started = True
            else:
                # finish previous microsaccade, if any
                if microsaccade_started:
                    new_microsaccade = (EyeMovementTypes.MICRO_SACCADE, microsaccade_start_idx, i)
                    found_events.append(new_microsaccade)
                    microsaccade_started = False

        # Finish up any open events
        if microsaccade_started:
            new_microsaccade = (EyeMovementTypes.MICRO_SACCADE, microsaccade_start_idx, len(velocities)-1)
            found_events.append(new_microsaccade)

        return found_events

    def check_binocularity_constrain(self, left: List[Tuple[EyeMovementTypes, int, int]],
                                     right: List[Tuple[EyeMovementTypes, int, int]]) -> List[Tuple[EyeMovementTypes, int, int]]:
        right_idx = np.array(right)
        for micro in left:
            if not (np.any(np.logical_and(micro[1] >= right_idx[:, 1], micro[1] <= right_idx[:, 2])) or np.any(
                    np.logical_and(
                        micro[2] >= right_idx[:, 1], micro[2] <= right_idx[:, 2]))):
                left.remove(micro)
        return left

    def detect(self, data: DataModel) -> None:
        sampling_frequency: float = data.sampling_frequency()

        if sampling_frequency < 250:
            print(
                "WARN: For detecting microsaccades you will need sampling frequencies >=250 Hz. Your data is sampled "
                "at %.1f Hz. This is likely to fail. Proceeding anyway, assuming you know what you are doing." %
                sampling_frequency)

        left_micro = []
        right_micro = []
        if self.require_binocular:
            assert DataModel.ET.LEFT_EYE_X in data.accessors and DataModel.ET.LEFT_EYE_Y in data.accessors and \
                   DataModel.ET.RIGHT_EYE_X in data.accessors and DataModel.ET.RIGHT_EYE_Y in data.accessors

            left_micro = self.detect_microsaccades(data.time(), data.get(DataModel.ET.LEFT_EYE_X),
                                                   data.get(DataModel.ET.LEFT_EYE_Y),
                                                   data.get(DataModel.ET.LEFT_EYE_VALID))
            right_micro = self.detect_microsaccades(data.time(), data.get(DataModel.ET.RIGHT_EYE_X),
                                                    data.get(DataModel.ET.RIGHT_EYE_Y),
                                                    data.get(DataModel.ET.RIGHT_EYE_VALID))
        else:
            left_micro = self.detect_microsaccades(data.time(), data.x(), data.y(), data.valid())
            right_micro = left_micro
        found_events = self.check_binocularity_constrain(left_micro, right_micro)

        # filter short microsaccades
        self.filter_short_microsaccades(data, found_events)

        # delete all previously detected microsaccades
        data.remove_all_events_of_type([EyeMovementTypes.MICRO_SACCADE])
        if data.events.size > 0:
            data.events = np.append(data.events, np.array(found_events), axis=0)
        else:
            data.events = np.array(found_events)

        print("Found %i Microsaccades." % (data.events_of_type(EyeMovementTypes.MICRO_SACCADE).shape[0]))

    def filter_short_microsaccades(self, data: DataModel, events: List[Tuple[EyeMovementTypes, int, int]]) -> None:
        for event in events:
            if Microsaccade(data, event[1], event[2]).duration < self.min_duration:
                events.remove(event)


class VelocityCalculatorEngelbert:
    """Calculates the average velocity between 5 samples.

    Note:
       Not sure whether it makes sense to always use 5 samples rather than using a time-window, but that's how the
       algorithm is defined. Especially for different frame-rates other implementations might make sense as well.
       But for comparability, we do it like that as well.

       Otero-Millan, Jorge, et al. "Unsupervised clustering method to detect microsaccades." Journal of vision 14.2 (
       2014): 18-18. actually suggest variable windows
    """

    @staticmethod
    def calculate(t: Sequence[float], x: Sequence[float], y: Sequence[float], valid: Sequence[bool]) -> np.array:
        """Calculates velocity estimates over a moving window of 5 samples. Code adapted from
        http://read.psych.uni-potsdam.de/index.php?option=com_content&view=article&id=140:engbert-et-al-2015
        -microsaccade-toolbox-for-r&catid=26:publications&Itemid=34 function vecvel in order to be as close to the
        reference implementation as possible.
        """
        assert len(t) == len(x) == len(y)

        # Reserve memory for the velocity list
        N = len(t)
        v = np.zeros((N, 2))
        sampling = 1000 / np.mean(np.diff(t))

        if len(t) < 5:
            print("Number of rows unreasonably small! Calculating velocities is not possible.")
            return v

        # We only implement type 2

        # GnuR indices are 1-based and include the first and last index in the slice
        # python indices are 0-based and include only the first index up to the previous-to-last index
        v[2:(N - 2), 0] = sampling / 6 * (x[4:N] + x[3:(N - 1)] - x[1:(N - 3)] - x[0:(N - 4)])
        v[1, 0] = sampling / 2 * (x[2] - x[0])
        v[N - 2, 0] = sampling / 2 * (x[N - 1] - x[N - 3])

        v[2:(N - 2), 1] = sampling / 6 * (y[4:N] + y[3:(N - 1)] - y[1:(N - 3)] - y[0:(N - 4)])
        v[1, 1] = sampling / 2 * (y[2] - y[0])
        v[N - 2, 1] = sampling / 2 * (y[N - 1] - y[N - 3])

        # set to nan where data validity is False
        # TODO necessary for all values included in the calculation! Not just the current one.
        # We could implement that by copying x and y and setting non-valid elements to nan.
        v[np.logical_not(valid)] = np.nan

        return v
