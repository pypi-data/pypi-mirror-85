from PerceptionToolkit.PluginInterfaces import IEventdetectionPlugin
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from typing import Sequence, Dict, Any
from PerceptionToolkit.EventdetectionHelpers import VelocityCalculatorPixels
from PerceptionToolkit.Version import Version
from pomegranate import HiddenMarkovModel, NormalDistribution, State, GeneralMixtureModel


class EventdetectionIHMM(IEventdetectionPlugin):
    """Performs event detection via machine learning by fitting either a HMM or GMM to the data.

    The implementation allows to fit either a hidden Markov model (HMM) with gaussian emissions or a Gaussian mixture
    model (GMM) to the eye movement velocities. The state/Gaussian with smaller mean is selected as the fixation state
    (as the eye is supposed not to move a lot), the other one as saccade state (where the eye moves at large
    velocities).

    We provide further post-processing functionality to filter short fixations and to merge sequential fixations.

    The Gaussian Mixture model is fitted to the eye velocities and via expectation maximization, contrary to
    implementations where not all data is available at the time of decision-making, e.g.:

    Kasneci, Enkelejda, et al. "Online recognition of fixations, saccades, and smooth pursuits for automated analysis
    of traffic hazard perception." Artificial neural networks. Springer, Cham, 2015. 411-434.
    """

    def __init__(self):
        super(EventdetectionIHMM, self).__init__()

        self.velocity_calculator_window = 20  # ms

        self.classifier_type = "HMM"
        self.merge_adjacent_fixations = True
        self.max_time_between_fixations = 75  # ms
        self.max_distance_between_fixations = 100  # same unit as dispersion

        self.discard_short_fixations = True
        self.min_fixation_duration = 60  # ms

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:

        self.velocity_calculator_window = parameters.get("velocity_calculator_window", self.velocity_calculator_window)

        self.classifier_type = parameters.get("classifier_type", self.classifier_type)
        assert self.classifier_type == "HMM" or self.classifier_type == "GMM"
        self.merge_adjacent_fixations = parameters.get("merge_adjacent_fixations", self.merge_adjacent_fixations)
        self.max_time_between_fixations = parameters.get("max_time_between_fixations", self.max_time_between_fixations)
        self.max_distance_between_fixations = parameters.get("max_distance_between_fixations",
                                                             self.max_distance_between_fixations)

        self.discard_short_fixations = parameters.get("discard_short_fixations", self.discard_short_fixations)
        self.min_fixation_duration = parameters.get("min_fixation_duration", self.min_fixation_duration)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def predict_state_sequence(self, velocities: Sequence[float]) -> (Sequence[int], int):
        # Define HMM
        n_states: int = 2
        fixation_index = 0

        feature_vector = np.array(velocities)

        # GMM and HMM cannot handle nans well. We just exclude them (although that perturbs the sequence a bit)
        nan_mask = np.isnan(feature_vector)
        nan_loc = np.where(~nan_mask)

        state_sequence = np.empty(len(feature_vector))
        state_sequence[:] = np.nan

        if self.classifier_type == "GMM":
            gmm = GeneralMixtureModel.from_samples([NormalDistribution, NormalDistribution], n_components=2,
                                                   X=feature_vector[~nan_mask].reshape(-1, 1))
            state_sequence_valid = gmm.predict(feature_vector[~nan_mask].reshape(-1, 1))
            state_sequence[nan_loc] = state_sequence_valid
            # find smaller mean (= expected velocity within a fixation)
            mue_0 = gmm.distributions[0].parameters[0]
            mue_1 = gmm.distributions[1].parameters[0]
            if mue_0 > mue_1:
                fixation_index = 1
        else:
            event_hmm = HiddenMarkovModel.from_samples(NormalDistribution, n_components=2,
                                                       X=feature_vector[~nan_mask].reshape(-1, 1))
            state_sequence_valid = event_hmm.predict(feature_vector[~nan_mask].reshape(-1, 1))
            state_sequence[nan_loc] = state_sequence_valid
            # find smaller mean (= expected velocity within a fixation)
            mue_0 = event_hmm.states[0].distribution.parameters[0]
            mue_1 = event_hmm.states[1].distribution.parameters[0]
            if mue_0 > mue_1:
                fixation_index = 1

        return state_sequence, fixation_index

    def process_state_sequence(self, state_sequence: Sequence[int], fixation_index: int, data: DataModel):
        # This code is identical to I-VT, with the only difference that it compares
        # the state instead of a velocity threshold.
        fixation_started: bool = False
        saccade_started: bool = False
        fixation_start_idx = 0
        saccade_start_idx = 0
        found_events = []
        i: int = 0
        for i in range(0, len(state_sequence)):
            if state_sequence[i] == fixation_index:
                # Fixation
                if not fixation_started:
                    # finish previous saccade, if any
                    if saccade_started:
                        new_saccade = (EyeMovementTypes.SACCADE, saccade_start_idx, i - 1)
                        assert saccade_start_idx >= 0
                        assert saccade_start_idx < data.raw.shape[0]
                        assert i >= 0
                        assert i < data.raw.shape[0]
                        # We do purposefully not enforce i < saccade_start_idx, as we want to be able to encode
                        # saccades that do not have a single sample assigned to them.
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
                        assert fixation_start_idx >= 0
                        assert fixation_start_idx < data.raw.shape[0]
                        assert i >= 0
                        assert i < data.raw.shape[0]
                        found_events.append(new_fixation)
                        fixation_started = False
                    saccade_start_idx = i
                    saccade_started = True

        # Finish up any open events
        if fixation_started:
            new_fixation = (EyeMovementTypes.FIXATION, fixation_start_idx, len(state_sequence) - 1)
            assert fixation_start_idx >= 0
            assert fixation_start_idx < data.raw.shape[0]
            assert i >= 0
            assert i < data.raw.shape[0]
            found_events.append(new_fixation)

        if saccade_started:
            new_saccade = (EyeMovementTypes.SACCADE, saccade_start_idx, len(state_sequence) - 1)
            assert saccade_start_idx >= 0
            assert saccade_start_idx < data.raw.shape[0]
            assert i >= 0
            assert i < data.raw.shape[0]
            found_events.append(new_saccade)

        # merge short nearby fixations
        fixations_before_merge = len(found_events)
        if self.merge_adjacent_fixations:
            IEventdetectionPlugin.merge_adjacent_fixations(found_events, data, self.max_time_between_fixations,
                                                           self.max_distance_between_fixations)
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

        print("Found %i Fixations and %i Saccades (%i merged, %i discarded)." % (
            data.fixations().shape[0], data.saccades().shape[0], fixations_merged, fixations_discarded))

    def detect(self, data: DataModel) -> None:
        # Calculate velocities
        vel_calc: VelocityCalculatorPixels = VelocityCalculatorPixels(self.velocity_calculator_window,
                                                                      data.sampling_frequency())

        t = data.time()
        x = data.x()
        y = data.y()
        v = data.valid()
        velocities: Sequence[float] = vel_calc.calculate(t, x, y, v)

        state_sequence, fixation_index = self.predict_state_sequence(velocities)

        self.process_state_sequence(state_sequence, fixation_index, data)
        #print(data.events)
        #data.test_events_consistency()
        #np.savetxt("ihmm.txt", data.events)
