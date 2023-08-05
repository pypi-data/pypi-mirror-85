from PerceptionToolkit.PluginInterfaces import IClassificationPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from typing import Sequence, Dict, Any, List, Tuple
import numpy as np
import random
from abc import ABC, abstractmethod
import math
import PerceptionToolkit.EyeMovements
from sklearn.model_selection import cross_val_score
from sklearn import svm
import sklearn.feature_selection
from functools import reduce

from os import path


class RangeTolerance:
    def __init__(self, value: float, tolerance: float):
        self.value = value
        self.tolerance = math.fabs(tolerance)

    def check(self, val: np.array) -> np.array:
        return np.fabs(self.value - val) <= self.tolerance


unique_pattern_id = 0


class Pattern(ABC):
    def __init__(self):
        super().__init__()
        self.id = -1
        self.score = 0
        self.set_unique_id()

    def set_unique_id(self):
        global unique_pattern_id
        self.id = unique_pattern_id
        unique_pattern_id += 1

    def mutate(self, parent):
        if random.random() < parent.mutation_rate:
            return self.mutate_impl(parent)
        return self

    def count_matches(self, sequence: int, parent) -> int:
        return len(self.get_matches(sequence, parent))

    def length(self) -> int:
        return 1

    @staticmethod
    @abstractmethod
    def get_random_instance(parent):
        pass

    @abstractmethod
    def mutate_impl(self, parent):
        pass

    @abstractmethod
    def get_matches(self, sequence: int, parent) -> Sequence[int]:
        """
        sequence refers to the index in the parent (ClassificationEvolutionaryPattern) sequence array used for
        caching the feature vectors
        """
        pass

    @staticmethod
    def random_range(limit_min: float, limit_max: float) -> RangeTolerance:
        x_1 = random.uniform(limit_min, limit_max)
        x_2 = random.uniform(limit_min, limit_max)
        val = (x_1 + x_2) / 2
        tol = math.fabs(x_1 - val)
        return RangeTolerance(val, tol)


class AggregatePattern(Pattern):
    def __init__(self, patterns: List):
        super().__init__()
        self.patterns: List[Pattern] = patterns

    @staticmethod
    def get_random_instance(parent):
        return AggregatePattern([parent.random_pattern(), parent.random_pattern()])

    def mutate_impl(self, parent):
        # determine which part of the pattern to mutate
        mutation_idx = random.randint(0, len(self.patterns) - 1)
        patterns_copy = self.patterns.copy()
        patterns_copy[mutation_idx] = patterns_copy[mutation_idx].mutate(parent)
        return AggregatePattern(patterns_copy)

    def get_matches(self, sequence: int, parent) -> Sequence[int]:
        matches = [p.get_matches(sequence, parent) for p in self.patterns]
        # this will also recursively check all subpatterns, in case they are aggregate patterns themselves

        for i in range(0, len(matches)):
            matches[i] -= self.patterns[i].length()  # subtract the length of the pattern, might be an aggregate itself.
        return reduce(np.intersect1d, matches)

    def length(self) -> int:
        return np.sum(np.array([p.length() for p in self.patterns]))


class FixationPattern(Pattern):
    def __init__(self, duration_range: RangeTolerance = RangeTolerance(0, 0),
                 x_loc_range: RangeTolerance = RangeTolerance(0, 0),
                 y_loc_range: RangeTolerance = RangeTolerance(0, 0)):
        super().__init__()
        self.duration_range = duration_range
        self.x_loc_range = x_loc_range
        self.y_loc_range = y_loc_range

    @staticmethod
    def get_random_instance(parent):
        return FixationPattern().mutate_location(parent).mutate_duration(parent)

    def mutate_impl(self, parent):
        if random.random() > 0.5:
            return self.mutate_location(parent)
        else:
            return self.mutate_duration(parent)

    def mutate_location(self, parent):
        x_loc_range = super().random_range(parent.x_location_range[0], parent.x_location_range[1])
        y_loc_range = super().random_range(parent.y_location_range[0], parent.y_location_range[1])
        return FixationPattern(self.duration_range, x_loc_range, y_loc_range)

    def mutate_duration(self, parent):
        duration_range = super().random_range(parent.duration_range[0], parent.duration_range[1])
        return FixationPattern(duration_range, self.x_loc_range, self.y_loc_range)

    def get_matches(self, sequence: int, parent) -> Sequence[int]:
        x_ok = self.x_loc_range.check(np.array(parent.x_location_sequence[sequence]))
        y_ok = self.y_loc_range.check(np.array(parent.y_location_sequence[sequence]))
        d_ok = self.duration_range.check(np.array(parent.duration_sequence[sequence]))
        matches = np.logical_and(np.logical_and(x_ok, y_ok), d_ok)

        return np.argwhere(matches)


class SaccadePattern(Pattern):
    def __init__(self, angle_range: RangeTolerance = RangeTolerance(0, 0),
                 amplitude_range: RangeTolerance = RangeTolerance(0, 0)):
        super().__init__()
        self.angle_range = angle_range
        self.amplitude_range = amplitude_range

    @staticmethod
    def get_random_instance(parent):
        return SaccadePattern().mutate_angle(parent).mutate_amplitude(parent)

    def mutate_impl(self, parent):
        if random.random() > 0.5:
            return self.mutate_angle(parent)
        else:
            return self.mutate_amplitude(parent)

    def mutate_angle(self, parent):
        angle_range = super().random_range(parent.angular_range[0], parent.angular_range[1])
        return SaccadePattern(angle_range, self.amplitude_range)

    def mutate_amplitude(self, parent):
        amplitude_range = super().random_range(parent.amplitude_range[0], parent.amplitude_range[1])
        return SaccadePattern(self.angle_range, amplitude_range)

    def get_matches(self, sequence: int, parent) -> Sequence[int]:
        a_ok = self.amplitude_range.check(np.array(parent.amplitude_sequence[sequence]))
        n_ok = self.angle_range.check(np.array(parent.direction_sequence[sequence]))
        matches = np.logical_and(a_ok, n_ok)
        return np.argwhere(matches)


class ClassificationEvolutionaryPattern(IClassificationPlugin):
    """
    Detects patterns that are discriminative between groups via a genetic evolutionary algorithm.
    Scoring is performed via correlation of pattern occurrences towards labels.
    Classification is performed based on the final pattern set and a SVM.
    """

    def __init__(self):
        super(ClassificationEvolutionaryPattern, self).__init__()
        self.number_of_generations = 100
        self.population_size = 10000
        self.mutation_rate = 0.1
        self.crossover_rate = 0.05
        self.number_selected_features = 30  # the number of (best in population) features to select for training
        
        # TODO implement elitism

        # These are just for caching so that calculations are sped up. They should not be set externally
        self.x_location_range = [float('inf'), float('-inf')]
        self.y_location_range = [float('inf'), float('-inf')]
        self.duration_range = [float('inf'), float('-inf')]
        self.angular_range = [0, 2 * math.pi]
        self.amplitude_range = [float('inf'), float('-inf')]

        self.x_location_sequence = []
        self.y_location_sequence = []
        self.duration_sequence = []
        self.amplitude_sequence = []
        self.direction_sequence = []

        self.classificator = None

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.number_of_generations = parameters.get("number_of_generations", self.number_of_generations)
        self.population_size = parameters.get("population_size", self.population_size)
        self.mutation_rate = parameters.get("mutation_rate", self.mutation_rate)
        self.number_selected_features = parameters.get("number_selected_features", self.number_selected_features)

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 1)

    def random_pattern(self) -> Pattern:
        pattern_types = [FixationPattern,
                         SaccadePattern]
        pattern_type_choice = pattern_types[random.randint(0, len(pattern_types) - 1)]
        return pattern_type_choice.get_random_instance(self)

    def init_population(self) -> List[Pattern]:
        patterns = []
        for i in range(0, self.population_size):
            patterns.append(self.random_pattern())
        return patterns

    def calculate_score(self, pattern: Pattern, data_idx: int) -> float:
        return pattern.count_matches(data_idx, self)

    def count_pattern_occurrences(self, patterns: List[Pattern]) -> np.array:
        occurrences = np.zeros((len(patterns), len(self.x_location_sequence)))
        for i, pattern in enumerate(patterns):
            for j in range(0, len(self.x_location_sequence)):
                occurrences[i, j] = self.calculate_score(pattern, j)
        return occurrences

    @staticmethod
    def unique_patterns_in_population(population: List[Pattern]) -> int:
        """
        Actually returns the number of patterns that are uniquely generated, not considering that by chance two
        identical patterns might be generated.
        """
        return len(set([p.id for p in population]))

    def label_vector(self, data: Sequence[DataModel]) -> List:
        return [int(d.meta[DataModel.META.LABEL]) for d in data]

    def evaluate(self, patterns: List[Pattern], data: Sequence[DataModel]) -> Tuple[np.array, List[int], float, float]:
        # count occurrences
        occurrences = self.count_pattern_occurrences(patterns)
        labels = self.label_vector(data)

        # An optimal score shows high differences between groups. The following options should in theory all work.
        # In practice, chi2 returns nans and therefore is non-optimal
        # scores = sklearn.feature_selection.chi2(occurrences.transpose(), labels)[0] # the chi2 statistics
        # scores = sklearn.feature_selection.f_classif(occurrences.transpose(), labels)[0]
        scores = sklearn.feature_selection.mutual_info_classif(occurrences.transpose(), labels)

        # We add an epsilon so that suboptimal patterns still have a (low) survivability
        epsilon = np.percentile(scores, 2)
        scores += epsilon

        for i, pattern in enumerate(patterns):
            pattern.score = scores[i]

        #print("Avg. population score %.3f(+/-%.3f)" % (np.nanmean(scores), 2 * np.nanstd(scores)))
        return occurrences, labels, np.nanmean(scores), 2 * np.nanstd(scores)

    def reproduce(self, population: List[Pattern]) -> List[Pattern]:
        # Select a random pattern to reproduce, based on its score (better scoring = more likely)
        # Reproduce
        new_population: List[Pattern] = []
        # Reserve those for cross-over mutations that are performed afterwards
        number_of_crossovers = int(self.crossover_rate * self.population_size)
        # Perform normal reproduction and point-mutation
        # some metrics might produce nans, therefore we need to be able to handle those.
        selection_boundaries: np.array = np.nancumsum([p.score for p in population])
        for i in range(0, self.population_size - number_of_crossovers):
            selection_value: float = random.uniform(0, np.max(selection_boundaries))
            selected_pattern = np.argwhere(selection_value <= selection_boundaries).flatten()
            selected_pattern = int(selected_pattern[0])
            new_population.append(population[selected_pattern].mutate(self))

        # Perform cross-over mutations / Linkage to longer patterns
        # TODO support actual cross-over of aggregate patterns as well
        for i in range(self.population_size - number_of_crossovers, self.population_size):
            # some metrics might produce nans, therefore we need to be able to handle those.
            selection_value_1: float = random.uniform(0, np.max(selection_boundaries))
            selection_value_2: float = random.uniform(0, np.max(selection_boundaries))
            selected_pattern_1 = np.argwhere(selection_value_1 <= selection_boundaries).flatten()
            selected_pattern_2 = np.argwhere(selection_value_2 <= selection_boundaries).flatten()
            selected_pattern_1 = int(selected_pattern_1[0])
            selected_pattern_2 = int(selected_pattern_2[0])
            new_population.append(AggregatePattern([population[selected_pattern_1], population[selected_pattern_2]]))

        return new_population

    def fit(self, data: Sequence[DataModel]) -> None:
        # Fill the ranges for available parameters
        print("Caching feature vectors")
        for d in data:
            fixations = [PerceptionToolkit.EyeMovements.Fixation(d, f[1], f[2]) for f in d.fixations()]
            saccades = [PerceptionToolkit.EyeMovements.Saccade(d, s[1], s[2]) for s in d.saccades()]
            centroids = [f.centroid for f in fixations]
            # cache data for performance (this will cache only one sequence)
            self.x_location_sequence.append(np.array(centroids)[:, 0])
            self.y_location_sequence.append(np.array(centroids)[:, 1])
            self.duration_sequence.append([f.duration for f in fixations])
            self.amplitude_sequence.append([s.amplitude for s in saccades])
            self.direction_sequence.append([s.direction for s in saccades])

            self.x_location_range[0] = min(self.x_location_range[0], np.min(self.x_location_sequence[-1]))
            self.x_location_range[1] = max(self.x_location_range[1], np.max(self.x_location_sequence[-1]))
            self.y_location_range[0] = min(self.y_location_range[0], np.min(self.y_location_sequence[-1]))
            self.y_location_range[1] = max(self.y_location_range[1], np.max(self.y_location_sequence[-1]))
            self.duration_range[0] = min(self.duration_range[0], np.min(self.duration_sequence[-1]))
            self.duration_range[1] = max(self.duration_range[1], np.max(self.duration_sequence[-1]))
            self.amplitude_range[0] = min(self.amplitude_range[0], np.min(self.amplitude_sequence[-1]))
            self.amplitude_range[1] = max(self.amplitude_range[1], np.max(self.amplitude_sequence[-1]))

        # Generate an initial set of patterns
        print("Initializing population")
        population: List[Pattern] = self.init_population()
        print("Starting to evolve")
        for generation in range(0, self.number_of_generations):
            features, labels, avg_score, std_score = self.evaluate(population, data)
            # Train classification on patterns
            # Extract high-scoring patterns
            self.classificator = svm.LinearSVC(max_iter=1000, dual=False)
            # The SVM can handle smaller feature spaces better
            features = sklearn.feature_selection.SelectKBest(sklearn.feature_selection.mutual_info_classif,
                                                             k=self.number_selected_features).fit_transform(
                features.transpose(), labels)
            scores = cross_val_score(self.classificator, features, labels, cv=5)
            number_unique_patterns = ClassificationEvolutionaryPattern.unique_patterns_in_population(population)
            print("Generation %i: %0.2f (+/- %0.2f) accuracy, %0.2f (+/- %0.2f) score, %i unique patterns of avg. length %0.1f" % (
            generation, scores.mean(), scores.std() * 2, avg_score, std_score, number_unique_patterns,
            np.mean(np.array([p.length() for p in population]))))

            file_path = 'output/evolution.txt'
            if path.exists(file_path):
                file = open(file_path, "a+")
            else:
                file = open(file_path, 'w+')
                file.write(
                    "generation scores_mean scores_std*2 avg_score std_score number_unique_patterns mean_length_population")
            to_save_ = [
                generation
                , scores.mean()
                , scores.std()*2
                , avg_score
                , std_score
                , number_unique_patterns
                , np.mean(np.array([p.length() for p in population]))
            ]
            file.write('\n' + ' '.join(map(str, to_save_)))
            file.close()

            # TODO save in textfile

            population = self.reproduce(population)

    def predict(self, data: DataModel) -> int:
        return 0
