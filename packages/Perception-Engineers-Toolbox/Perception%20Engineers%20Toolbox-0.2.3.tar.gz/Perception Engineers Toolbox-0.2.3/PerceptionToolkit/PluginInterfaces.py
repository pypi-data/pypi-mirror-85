from yapsy.PluginManager import IPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from PerceptionToolkit.EyeMovements import Fixation
from typing import Sequence, List, Tuple, Dict, Any
import numpy as np
from PerceptionToolkit import Version
from abc import abstractmethod, ABC


class IToolboxPlugin(IPlugin, ABC):
    """This is the general interface for all plugins. Any new plugin types should inherit IToolboxPlugin."""

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        """Applies a set of parameters to the plugin. The plugin can query those by name from the provided dict. This is
         not limited to literals but can also contain substructures."""
        pass

    @staticmethod
    @abstractmethod
    def version() -> Version:
        pass


class IPersistencePlugin(IToolboxPlugin, ABC):
    """Handles data import and export.

    As there is a plethora of eye-tracking data formats, we need a similar variety of import code.
    The supplied plugins contain ways to load text-file CSV formatted data (PersistenceCSV) in an almost arbitrary
    format. However, I have already encountered plenty of formats that cannot be read / split into trials via that code.
    In such a case, please write your own plugin / modify the provided ones.

    For saving data, I would recommend a binary data format. It is not human readable, however you are not supposed to
    manipulate it by hand anyways. However, reading and writing speed are significantly faster.

    You can also utilize these plugins to convert between different data formats (i.e., read with one plugin, write with
    another).

    Returns:
        A list of data trials read
    """

    def read(self) -> List[DataModel]:
        """Loads one recording file containing one or more trials. Each trial is returned as a separate DataModel
        object. """
        pass

    def write(self, data: Sequence[DataModel]) -> None:
        """Writes data objects to file, e.g., for export. The plugin might need different parameters than during
        reading, such as the target file name for each recording"""
        pass

    @staticmethod
    def report(data: DataModel) -> None:
        """Provides a short summary of what happened during data loading"""
        print("Imported %i samples (%.0fs @ %.1fHz) with %i columns." % (
            data.sample_count(), data.duration() / 1000, data.sampling_frequency(), len(data.raw.columns)))

    @staticmethod
    def report_final(data: List[DataModel]) -> None:
        """Provides a short summary of what happened during data loading"""
        if len(data) > 1:
            print("Imported %i trials." % len(data))


class ITrialFilterPlugin(IToolboxPlugin, ABC):
    """Handles the selection of a subset of trials via quality or metadata.
    Returns:
        A list of data trials read
    """

    def filter(self, data: List[DataModel]) -> List[DataModel]:
        """Loads one recording file containing one or more trials. Each trial is returned as a separate DataModel
        object. """
        pass


class IPreprocessingPlugin(IToolboxPlugin, ABC):
    def process(self, data: DataModel) -> None:
        """Applies some pre processing (such as filtering or interpolation) to the raw data.
        Popular examples are blink removal, gap interpolation or smoothing"""
        pass


class IEventdetectionPlugin(IToolboxPlugin, ABC):
    def detect(self, data: DataModel) -> None:
        """Detect different eye movement types in the raw data.

        These are written into the DataModel's event field.

        Any previously detected events are overwritten.
        You can detect more than one eye-movement type within the same EventdetectionPlugin if your algorithm is able
        to do so.

        Note:
            For custom implementations it would make sense to keep track of events as a list of
            (EyemovementType, startIdx, endIdx)as merging and filtering is fast within lists (especially deleting a
            row). When done, it needs to be converted to a numpy array to feed it into the DataModel.
        """

        pass

    @staticmethod
    def discard_short_fixations(event_list: List[Tuple[EyeMovementTypes, int, int]], data: DataModel,
                                min_fixation_duration: float) -> None:
        """Some event filters allow for arbitrary length fixations. This function can be applied to make sure fixation
        have a certain minimal duration. If combined with a merging step (merge_adjacent_fixations) you might want to
        merge before removing short fixations, as merging makes them longer.

        Note:
            This does NOT merge saccades before and after the discarded short fixation (because I do not think that this
            would be a good idea, but I do understand that this is open to discussion). Therefore, the number of
            saccades may exceed the number of fixations after this step.
        """
        removed_fixations: int = 0

        total_fixations: int = 0
        for event in event_list:
            if event[0] == EyeMovementTypes.FIXATION:
                total_fixations += 1

        i: int = 0
        while i < len(event_list) - 1:  # the last sample cannot be merged to its successor (as it has none)
            if event_list[i][0] == EyeMovementTypes.FIXATION:
                if Fixation(data, event_list[i][1], event_list[i][2]).duration < min_fixation_duration:
                    del event_list[i]
                    # it would be possible to handle surrounding saccades somehow.
                    i -= 1
                    removed_fixations += 1
            i += 1

        # This is done for sanity checking only
        total_fixations_after: int = 0
        for event in event_list:
            if event[0] == EyeMovementTypes.FIXATION:
                total_fixations_after += 1

        # print("Discarded %i short fixations (before %i -> after %i)" % (
        #    removed_fixations, total_fixations, total_fixations_after))

    @staticmethod
    def merge_adjacent_fixations(event_list: List[Tuple[EyeMovementTypes, int, int]], data: DataModel,
                                 max_time_between_fixations: float,
                                 max_distance_between_fixations: float) -> None:
        """Sometimes fixation filters might produce two distinct fixations that are very close temporally as well as
        spatially (e.g., when there is a gap in the data or no filtering was applied beforehand). This function fuses
        such fixations that are likely to be just one single fixation together.

        Also deletes saccades in-between two merged fixations, as their samples are re-assigned to the fixation.
        """
        merged_fixations: int = 0

        total_fixations: int = 0
        for event in event_list:
            if event[0] == EyeMovementTypes.FIXATION:
                total_fixations += 1

        i: int = 0
        j: int = 1
        while i < len(event_list) - 1 and j < len(event_list) - 1:  # the last sample cannot be merged to its
            # successor (as it has none)
            # make sure we compare two subsequent fixations
            if j <= i:
                j = i + 1
            if not event_list[i][0] == EyeMovementTypes.FIXATION:
                i += 1
                continue
            if not event_list[j][0] == EyeMovementTypes.FIXATION:
                j += 1
                continue

            f1 = Fixation(data, event_list[i][1], event_list[i][2])
            f2 = Fixation(data, event_list[j][1], event_list[j][2])
            time_between_fixations: float = f2.startTime - f1.endTime  # start of second - end of first
            if time_between_fixations < max_time_between_fixations:
                distance_between_fixations = np.linalg.norm(np.array(f1.centroid) - np.array(f2.centroid))
                if distance_between_fixations < max_distance_between_fixations:
                    event_list[i] = (event_list[i][0], event_list[i][1], event_list[j][2])
                    del event_list[i + 1:j + 1]
                    merged_fixations += 1
                    i -= 1
                    j = i + 1
            i += 1

        # This is done for sanity checking only
        total_fixations_after: int = 0
        for event in event_list:
            if event[0] == EyeMovementTypes.FIXATION:
                total_fixations_after += 1

        # print("Merged %i fixations (before %i -> after %i)" % (
        #    merged_fixations, total_fixations, total_fixations_after))


class IVisualizationPlugin(IToolboxPlugin, ABC):
    """Draws an image of some kind from the data"""

    def draw(self, data: Sequence[DataModel]) -> np.array: pass


class IClassificationPlugin(IToolboxPlugin, ABC):
    """Performs group label prediction based on scanpath data"""

    def fit(self, data: Sequence[DataModel]) -> None:
        """Performs the training step of a machine learning approach or any method to allow for the later classification
        of a single scanpath to a group label. Assumes that the meta property "label" is set in all provided models."""
        pass

    def predict(self, data: DataModel) -> int:
        """Provides a group label estimate for the scanpath. Make sure to call the fitting step before attempting a
        prediction."""
        pass


class IMetricPlugin(IToolboxPlugin, ABC):
    """Calculates metrics on the data, such as average fixation duration, scanpath length,..."""

    def calculate(self, data: DataModel) -> None:
        """Provides a characteristic metric of some kind (e.g., average fixation duration, fixation count,...).

        Metrics are written to the DataModel's metric field to be accessible after calculation.
        """
        pass
