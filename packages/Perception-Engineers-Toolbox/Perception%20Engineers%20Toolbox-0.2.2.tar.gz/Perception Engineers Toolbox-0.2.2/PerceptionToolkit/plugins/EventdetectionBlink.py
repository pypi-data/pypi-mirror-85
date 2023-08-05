from PerceptionToolkit.PluginInterfaces import IEventdetectionPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from typing import Sequence, List, Tuple, Any, Dict
import numpy as np
from typing import Dict, Sequence, Any


class EventdetectionBlink(IEventdetectionPlugin):
    """
    A simple approach to detect blinks in the data set.

    The general setup and the choice of the parameters is from Eye Tracking: A comprehensive Guide to Methods and
    Meausres (Holmqvist et al. 2011). See section 5.7 for Blink detection. In this source, min_blink_lenghts of 50-100
    ms are recommended as well as marking the 120 ms which precede and follow a blink as invalid.

    Attributes:
        min_blink_length: The minimum duration of continuous invalid data to detect a blink (given in ms).
        invalid_area: The time (in ms) for which data are marked invalid before and after a detected blink, because
        otherwise a downward saccade would have been detected douring the closing and opening process.
    """

    def __init__(self):
        super(EventdetectionBlink, self).__init__()
        self.min_blink_length = 22  # ms
        self.invalid_area = 42 # ms

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.min_blink_length = parameters.get("min_blink_length", self.min_blink_length)
        self.invalid_area = parameters.get("invalid_area", self.invalid_area)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def mark_invalid_data(self, data: DataModel) -> None:
        """The values of the part that precedes and the part that follows the detected blinks are set invalid. In order to
        do so, for every Blink event a lower and an upper threshold are calculated as a reference."""
        for i in range(len(data.events)):
            if data.events[i,0] == 6:
                lowerThreshold = data.time()[data.events[i,1]] - self.invalid_area
                upperThreshold = data.time()[data.events[i,2]] + self.invalid_area
                for j in range(data.events[i, 1]+1):
                    if data.time()[j] > lowerThreshold:
                        data.raw[j, data.accessors[DataModel.ET.LEFT_EYE_VALID]] = False
                        data.raw[j, data.accessors[DataModel.ET.RIGHT_EYE_VALID]] = False
                for l in range(data.events[i, 2], len(data.raw)):
                    if data.time()[l] < upperThreshold:
                        data.raw[l, data.accessors[DataModel.ET.LEFT_EYE_VALID]] = False
                        data.raw[l, data.accessors[DataModel.ET.RIGHT_EYE_VALID]] = False

    def write_event(self, detected_blinks,data: DataModel) -> None:
        """The detected blink events are added to data.events"""
        found_events = []
        for i in range(len(detected_blinks)):
            found_events.append([EyeMovementTypes.BLINK, detected_blinks[i][1] - (detected_blinks[i][0]-1), detected_blinks[i][1]])
        if data.events.size == 0:
            data.events = np.array(found_events)
        else:
            data.remove_all_events_of_type([EyeMovementTypes.BLINK])
            data.events = np.append(data.events, np.array(found_events), axis=0)
        print("Found %i Blinks." % (data.events_of_type(EyeMovementTypes.BLINK).shape[0]))
        self.mark_invalid_data(data)

    # filter out the real blinks from possible blinks area
    def check_time(self, blinks, data: DataModel):
        """The potential blinks are compared with min_blink_length and the detected blinks are stored in the
        detected_blinks-list"""
        detected_blinks = []
        for i in blinks:
            if data.time()[i[1]]-data.time()[i[1]-i[0]-1] >= self.min_blink_length:
                detected_blinks.append(i)
        self.write_event(detected_blinks, data)

    def detect(self, data: DataModel) -> None:
        counter = 0
        blinks = []
        # calculate the potiential blinks and store them in the list of blinks
        for i in range(len(data.raw)):
            if data.valid()[i] and (counter != 0):
                blinks.append([counter, i-1])
                counter = 0
            if not data.valid()[i]:
                counter += 1
        self.check_time(blinks, data)