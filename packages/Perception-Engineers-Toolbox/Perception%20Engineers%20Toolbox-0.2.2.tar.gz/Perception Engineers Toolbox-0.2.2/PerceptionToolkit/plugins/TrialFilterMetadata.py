from PerceptionToolkit.PluginInterfaces import ITrialFilterPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from typing import List, Dict, Any
import numpy as np


class TrialFilterMetadata(ITrialFilterPlugin):
    """Filters trials by specific metadata properties

    IN DEVELOPMENT! DO NOT USE IN PRODUCTION!
    UNTESTED! (But might work)

    It only makes sense to use either the include or the exclude list of one property. Different properties can be
    combined arbitrarily (e.g. filter for "Subject 1" and "Subject 2" and exclude the trial "Fixation cross")

    Attributes:
        keep_trials_list: Trials that should explicitly be kept (all others are removed)
        exclude_trials_list: Trials that should explicitly be excluded (all others are kept)

        keep_labels_list: Keeps only trials with matching labels
        exclude_labels_list: Excludes trials with those labels

        keep_subjects_list: Keep only trials of those subjects
        exclude_subjects_list: Remove trials of those subjects
    """

    def __init__(self):
        super(TrialFilterMetadata, self).__init__()
        self.keep_trials_list = []
        self.exclude_trials_list = []

        self.keep_labels_list = []
        self.exclude_labels_list = []

        self.keep_subjects_list = []
        self.exclude_subjects_list = []

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.keep_trials_list = parameters.get("keep_trials_list", self.keep_trials_list)
        self.exclude_trials_list = parameters.get("exclude_trials_list", self.exclude_trials_list)
        self.keep_labels_list = parameters.get("keep_labels_list", self.keep_labels_list)
        self.exclude_labels_list = parameters.get("exclude_labels_list", self.exclude_labels_list)
        self.keep_subjects_list = parameters.get("keep_subjects_list", self.keep_subjects_list)
        self.exclude_subjects_list = parameters.get("exclude_subjects_list", self.exclude_subjects_list)

        # Make sure no trial is supposed to be both kept and excluded
        for trial in self.keep_trials_list:
            assert trial not in self.exclude_trials_list
        for label in self.keep_labels_list:
            assert label not in self.exclude_labels_list
        for subject in self.keep_subjects_list:
            assert subject not in self.exclude_subjects_list

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 2)

    def filter(self, data: List[DataModel]) -> List[DataModel]:
        selector = lambda meta, mylist: map(lambda t: t.meta[meta] in mylist, data)
        merger = lambda meta, mylist, add_to: np.logical_and(selector(meta, mylist), add_to) if mylist else add_to

        keep_list = np.ones(len(data))
        exclude_list = np.zeros(len(data))
        merger("trial", self.keep_trials_list, keep_list)
        merger("trial", self.exclude_trials_list, exclude_list)
        merger("label", self.keep_labels_list, keep_list)
        merger("label", self.exclude_labels_list, exclude_list)
        merger("subject", self.keep_subjects_list, keep_list)
        merger("subject", self.exclude_subjects_list, exclude_list)
        keep_list = np.logical_and(keep_list, np.logical_not(exclude_list))
        print("Removed " + str(len(data) - np.sum(keep_list)) + "/" + str(len(data)) + " trials based on metadata.")
        return data[keep_list]
