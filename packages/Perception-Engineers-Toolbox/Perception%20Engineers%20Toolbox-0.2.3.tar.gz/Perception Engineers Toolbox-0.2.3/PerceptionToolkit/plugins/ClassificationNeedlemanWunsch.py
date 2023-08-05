from sklearn.metrics import confusion_matrix

from PerceptionToolkit import Version
from PerceptionToolkit.PluginInterfaces import IClassificationPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovements import Fixation

from typing import Sequence, Dict, Any, Union
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance
from scipy.spatial import distance

import timeit
import os

class ClassificationNeedlemanWunsch(IClassificationPlugin):
    """
    Needleman-Wunsch (ScanMatch)
    Based on: https://link.springer.com/article/10.3758/BRM.42.3.692
    The scanpath is compared pairwise to every other scanpath in the set using the Needleman-Wunsch string
    alignment algorithm. Prediction is done via KNN.

    Attributes:
        gap_penalty: penalty score for each gap in the scanpath
        horizontal_alphabet_size: number of bins in the image along the x-axis
        vertical_alphabet_size: number of bins in the image along the y-axis
        image_dimensions: dimension of the image
        sampling: sampling size for the fixation duration
        enable_duration: specify whether the fixation should be repeated respective of its duration
        k_nearest: the number of most similar scanpaths to the given scanpath
        enable_plot: specify whether to represent the data in graphical format
        subs_mat: specify whether to create a basic or euclidean-based substitution matrix
    """

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 1)

    def __init__(self):
        super(ClassificationNeedlemanWunsch, self).__init__()
        # User determinable
        self.gap_penalty: int = 0
        self.horizontal_alphabet_size: int = 5
        self.vertical_alphabet_size: int = 3
        self.image_dimensions: tuple = None
        self.sampling: int = 100
        self.enable_duration: bool = True
        self.k_nearest: int = 5
        self.subs_mat: str = 'basic'
        self.substitution_matrix = None

        self.enable_plot: bool = False  # for visualization purposes

        self.candidates: int = None
        self.enable_filter: bool = False
        self.filter_method: str = 'intersect'

        self.scoring_mats = []
        self.distance_matrix = []
        self.features = []
        self.labels = []
        self.encoding_boundaries_x = None
        self.encoding_boundaries_y = None

        # temporary
        # self.truth = None

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.gap_penalty = parameters.get("gap_penalty", self.gap_penalty)
        self.horizontal_alphabet_size = parameters.get("horizontal_alphabet_size", self.horizontal_alphabet_size)
        self.vertical_alphabet_size = parameters.get("vertical_alphabet_size", self.vertical_alphabet_size)
        assert self.horizontal_alphabet_size > 0 and self.vertical_alphabet_size > 0, "Alphabet size must be greater than 0."
        self.image_dimensions = parameters.get("image_dimensions", self.image_dimensions)
        # assert 0 not in self.image_dimensions, "Inappropriate image dimension."
        self.sampling = parameters.get("sampling", self.sampling)
        assert self.sampling > 0, "Sampling must be greater than zero."
        self.enable_duration = parameters.get("enable_duration", self.enable_duration)
        self.k_nearest = parameters.get("k_nearest", self.k_nearest)
        assert self.k_nearest > 0, "Nearest neighbors must be greater than 0."
        self.enable_plot = parameters.get("enable_plot", self.enable_plot)
        self.subs_mat = parameters.get("subs_mat", self.subs_mat)
        assert self.subs_mat in ['basic', 'euclidean']
        self.substitution_matrix = parameters.get("substitution_matrix", self.substitution_matrix)
        self.candidates = parameters.get("candidates", self.candidates)
        self.enable_filter = parameters.get("enable_filter", self.enable_filter)
        self.filter_method = parameters.get("filter_method", self.filter_method)
        assert self.filter_method in ['jensenshannon', 'wasserstein', 'euclidean', 'chebyshev', 'cityblock', 'intersect']

    def find_boundaries(self, data: Sequence[DataModel]) -> tuple:
        # if image dimensions not manually set, find the minimum/maximum x/y coordinates to determine the boundaries for
        # the image binning

        if self.image_dimensions is not None:
            print("Detected manually set image dimensions")
            self.encoding_boundaries_x = np.linspace(0, self.image_dimensions[0], self.horizontal_alphabet_size + 1)[1:]
            self.encoding_boundaries_y = np.linspace(0, self.image_dimensions[1], self.vertical_alphabet_size + 1)[1:]
            return 0, 0, self.image_dimensions[0], self.image_dimensions[1]

        print("Automatically determining image dimensions")
        min_x: int = np.Inf
        min_y: int = np.Inf
        max_x: int = -np.Inf
        max_y: int = -np.Inf

        # update all the values
        for scanpath in data:
            # extracts a list of fixations from the datamodel. fixation := [centroid: (int, int), duration: int]
            fixations_centroid = np.apply_along_axis(
                lambda f: Fixation(scanpath, f[1], f[2]).centroid, 1,
                scanpath.fixations())
            temp_minx = min(fixations_centroid, key=lambda x: x[0])[0]
            temp_miny = min(fixations_centroid, key=lambda x: x[1])[1]
            temp_maxx = max(fixations_centroid, key=lambda x: x[0])[0]
            temp_maxy = max(fixations_centroid, key=lambda x: x[1])[1]
            min_x = min(min_x, temp_minx)
            min_y = min(min_y, temp_miny)
            max_x = max(max_x, temp_maxx)
            max_y = max(max_y, temp_maxy)

        self.encoding_boundaries_x = np.linspace(min_x, max_x, self.horizontal_alphabet_size + 1)[1:]
        self.encoding_boundaries_y = np.linspace(min_y, max_y, self.vertical_alphabet_size + 1)[1:]

        print("Detected boundaries: ({}, {}) ({}, {})".format(min_x, min_y, max_x, max_y))
        return min_x, min_y, max_x, max_y

    def calculate_substitution_matrix(self, len_ROIs: int):
        # Takes the total number of ROIs and creates a substitution matrix of 1's and -1's

        if 'basic' in self.subs_mat:
            self.substitution_matrix = np.full((len_ROIs, len_ROIs), -1)
            np.fill_diagonal(self.substitution_matrix, 1)
        else:
            self.substitution_matrix = np.zeros((len_ROIs, len_ROIs))
            for c in range(self.horizontal_alphabet_size):
                for r in range(self.vertical_alphabet_size):
                    vertical_loc = (r * self.horizontal_alphabet_size) + c
                    for cc in range(self.horizontal_alphabet_size):
                        for rr in range(self.vertical_alphabet_size):
                            horizontal_loc = (rr * self.horizontal_alphabet_size) + cc
                            if vertical_loc == horizontal_loc:
                                dist = 1
                            else:
                                # get euclidean distance between two ROIs
                                dist = -int(np.linalg.norm(np.array((c, r)) - np.array((cc, rr))))
                            self.substitution_matrix[vertical_loc, horizontal_loc] = dist
        # print(self.substitution_matrix)
        return self.substitution_matrix

    def encode_fixation(self, fix) -> list:
        # Takes a fixation (centroid, duration) and encodes it into a repeating integer

        centroid, duration = 0, 1

        x = np.argmax(fix[centroid][0] <= self.encoding_boundaries_x)
        y = np.argmax(fix[centroid][1] <= self.encoding_boundaries_y)

        # calculate ROI position using 2D row-major order: offset = (row_index * TotalCols) + col_index
        roi: int = (y * self.horizontal_alphabet_size) + x

        repeat: int = int(fix[duration] / self.sampling)

        return [roi for _ in range(repeat)] if self.enable_duration else [roi]

    def encode(self, scanpath: DataModel) -> list:
        # Encodes a given scanpath into a list of integers

        # extracts a list of fixations from the datamodel. fixation := [centroid: (int, int), duration: int]
        fixations_centroid_duration = np.apply_along_axis(
            lambda f: [Fixation(scanpath, f[1], f[2]).centroid, Fixation(scanpath, f[1], f[2]).duration], 1,
            scanpath.fixations())

        scanpath_ = []

        # converts each fixation into a list of repeating (if duration enabled) integer and extends it to the scanpath
        for fix in fixations_centroid_duration:
            scanpath_.extend(self.encode_fixation(fix))

        return scanpath_

    def filter_by_distance(self, sp1: Sequence[int]):
        # Filters out too distant training data according to a distance metric
        # assumption: all scanpaths are already encoded

        assert len(self.features) > 0, "Features must not be empty."
        if self.candidates is None:
            # take all data up to median
            n = int((len(self.features) + self.k_nearest) / 2)
        else:
            assert self.k_nearest <= self.candidates <= len(self.features)
            print('Candidates detected ', self.candidates)
            n = self.candidates

        intersect = lambda x, y: np.true_divide(np.sum(np.minimum(x, y)), np.sum(x))
        method = {"jensenshannon": distance.jensenshannon
                , "chebyshev": distance.chebyshev
                , "cityblock": distance.cityblock
                , "wasserstein": wasserstein_distance
                , "euclidean": distance.euclidean
                , "intersect": intersect
                  }.get(self.filter_method, lambda: "Invalid method")

        norm = lambda x: x / np.linalg.norm(x)
        dists = np.asarray([method(
            norm(np.bincount(sp1, minlength=self.horizontal_alphabet_size * self.vertical_alphabet_size)),
            norm(np.bincount(sp2, minlength=self.horizontal_alphabet_size * self.vertical_alphabet_size))) for sp2 in
            self.features])

        # gets index of n closest scanpaths by ROI occurence
        if 'intersect' in self.filter_method:
            idx = np.argpartition(dists, len(dists)-n)[-n:]
        else:
            idx = np.argpartition(dists, n)[:n]
        print("length idx:", len(idx))

        filtered_features = [self.features[i] for i in idx]
        filtered_labels = [self.labels[i] for i in idx]

        print('''
        Prefiltering training data...
        Calculating n ... : {}
        {}/{} saved for comparison.
        Remaining labels: {}
        '''.format(n
                   , len(filtered_features)
                   , len(self.features)
                   , len(filtered_labels)
                   )
              )

        return filtered_features, filtered_labels

    def align(self, score_mat, sp1, sp2):
        # shows best alignment for two scanpaths given a scoring matrix. Must call compare_pairwise method beforehand
        # this method is solely used for the visual representation of the alignment of two scanpaths and does not really
        # play any role outside this script.

        align_a = ""
        align_b = ""
        offset = 1
        i = len(sp1)
        j = len(sp2)

        while i > 0 or j > 0:
            if i > 0 and j > 0 and \
                    score_mat[j, i] == score_mat[j - 1, i - 1] + self.get_match_score(j - offset, i - offset, sp1, sp2):
                align_a = str(sp1[i - offset]) + align_a
                align_b = str(sp2[j - offset]) + align_b
                i -= 1
                j -= 1
            elif i > 0 and score_mat[j, i] == score_mat[j - 1, i] + self.gap_penalty:
                align_a = str(sp1[i - offset]) + align_a
                align_b = "--" + align_b
                i -= 1
            else:
                align_a = "--" + align_a
                align_b = str(sp2[j - offset]) + align_b
                j -= 1

        print("Alignment")
        # for i in range(0, len(alignA)):
        #     print(alignA[i] + " <-> " + alignB[i] )
        print(align_a)
        print(align_b)

    def compare_needlemanwunsch(self, scanpath1: Sequence[int], scanpath2: Sequence[int]) -> float:
        # after NMW comparison, the scoring matrix is then appended to the attribute self.scoring_mats

        m_width: int = len(scanpath1)
        m_height: int = len(scanpath2)
        scoring_matrix = np.zeros((m_height + 1, m_width + 1))

        # filling first col and row
        for c in range(1, m_width + 1):
            scoring_matrix[0, c] = scoring_matrix[0, c - 1] + self.gap_penalty
        for r in range(1, m_height + 1):
            scoring_matrix[r, 0] = scoring_matrix[r - 1, 0] + self.gap_penalty

        # filling the rest
        offset = 1  # with respect to theta in substitution matrix
        for c in range(offset, m_width + offset):
            for r in range(offset, m_height + offset):
                scoring_matrix[r, c] = max(
                    scoring_matrix[r - 1, c - 1] + self.get_match_score(r - offset, c - offset, scanpath1, scanpath2)
                    # diagonal
                    , scoring_matrix[r - 1, c] + self.gap_penalty  # up
                    , scoring_matrix[r, c - 1] + self.gap_penalty  # left
                )

        self.scoring_mats.append(scoring_matrix)

        return self.get_score(scoring_matrix, scanpath1, scanpath2)

    def get_match_score(self, row: int, col: int, sp1: Sequence[int], sp2: Sequence[int]) -> int:
        return self.substitution_matrix[sp2[row], sp1[col]]

    def get_score(self, score_mat, sc1, sc2) -> float:
        # takes the maximum alignment score from the scoring matrix and returns the normalized score

        score = score_mat[-1, -1]
        max_sub_score = np.max(self.substitution_matrix)
        max_len = max(len(sc1), len(sc2))

        return score / (max_sub_score * max_len)

    def calculate_distance_matrix(self, data: Sequence[DataModel]) -> None:
        ### Creating a nxn distance matrix
        # Initialize an empty nxn distance matrix
        # Create substitution matrix
        # Fill up the distance matrix (commented out because not really useful. Might do away with distance_matrix)
        progress = ""
        print("Generating distance matrix:")

        self.distance_matrix = np.zeros((len(data), len(data)))
        self.calculate_substitution_matrix(self.horizontal_alphabet_size * self.vertical_alphabet_size)

        for scanpath in data:
            self.features.append(self.encode(scanpath))
            self.labels.append(scanpath.meta[DataModel.META.LABEL])

        for i, scanpath1 in enumerate(self.features):
            progress += "▉"
            print(progress)
            for j, scanpath2 in enumerate(self.features[i:]):  # assume: commutative relationship
                self.distance_matrix[i + j, i] = self.compare_needlemanwunsch(scanpath1, scanpath2)

        if self.enable_plot:
            ticks = ["t{}_s{}_sb{}".format(sp.meta[DataModel.META.LABEL]
                                           , sp.meta[DataModel.META.STIMULUS]
                                           , sp.meta[DataModel.META.SUBJECT]
                                           ) for sp in data]
            plt.imshow(self.distance_matrix, cmap="nipy_spectral")
            plt.colorbar()
            plt.clim(0, 1)
            plt.xticks(np.arange(len(data)), ticks, rotation="vertical")
            plt.yticks(np.arange(len(data)), ticks)

            plt.show()
            plt.close()

    def fit(self, data: Sequence[DataModel]) -> None:
        """
        Extracts and encodes the scanpath from each datamodel. Each scanpath and its corresponding label is stored
        for the prediction step.

        :param data: Sequence[DataModel]
        :return: None
        """
        # ------ Steps: ------
        # Reset the features and labels
        # Save features and labels of each scanpath in data

        self.find_boundaries(data)

        self.features = []
        self.labels = []

        for scanpath in data:
            self.features.append(self.encode(scanpath))
            self.labels.append(scanpath.meta[DataModel.META.LABEL])

    def predict(self, data: DataModel) -> int:
        """
        Predicts the label of given data based on set specified in fit-step (using NMW and KNN)

        :param
        data: DataModel
            The datamodel to be predicted
        :return:
        prediction: int
            The predicted label
        """

        # # TEMP
        # self.truth = data.meta[DataModel.META.LABEL]

        # ------ Steps: ------
        # Initialize empty distance array
        # Encode the scanpath from the datamodel
        # Compare (using NMW) the scanpath to every other scanpath saved in the list, add score to the distance array
        # Get index of k-nearest neighbors to scanpath
        # Get most frequently occurring label =: prediction
        # Save prediction in datamodel metric

        # check if user defined a substitution matrix beforehand. Otherwise, create its own.
        if self.substitution_matrix is None:
            self.calculate_substitution_matrix(self.horizontal_alphabet_size * self.vertical_alphabet_size)

        sp1 = self.encode(data)

        # filter out the features according to distance with test data
        if self.enable_filter:
            print("Prefiltering data.")
            filtered_features, filtered_labels = self.filter_by_distance(sp1)
        else:
            print("Prefilter disabled. Skipping step...")
            filtered_features = self.features
            filtered_labels = self.labels

        # array containing distances to scanpath in question
        dist_to_sp1 = np.zeros(len(filtered_features))
        print("Features length {}".format(len(filtered_features)))

        for l, scanpath in enumerate(filtered_features):
            dist_to_sp1[l] = self.compare_needlemanwunsch(sp1, scanpath)

        # get index of k nearest scanpaths (biggest NMW score) !!! the result is unsorted
        k_nearest_index = np.argpartition(dist_to_sp1, -self.k_nearest)[-self.k_nearest:]

        nearest_distance = [dist_to_sp1[i] for i in k_nearest_index]
        nearest_labels = [filtered_labels[i] for i in k_nearest_index]
        print("k={} Nearest neighbors: {}".format(self.k_nearest, nearest_labels))
        print("Nearest distance: {}".format(nearest_distance))

        # get the most frequently occurring label
        prediction = np.argmax(np.bincount(nearest_labels))

        # data.metrics["prediction"] = int(prediction)
        data.metrics["prediction"] = prediction

        # print("Predicted label: {}".format(prediction))
        # print("True label: {}".format(data.meta[DataModel.META.LABEL]))

        if self.enable_plot:
            plt.imshow(dist_to_sp1.reshape(1, -1), cmap='cool')
            plt.colorbar(orientation='horizontal')
            plt.clim(min(dist_to_sp1), max(dist_to_sp1))
            plt.xticks(np.arange(len(self.features)), self.labels)
            plt.yticks(np.arange(1), [data.meta[DataModel.META.LABEL]])
            plt.ylabel("True label")
            plt.xlabel("Predicted label")
            plt.title("Prediction using KNN (k={})".format(self.k_nearest))

            plt.show()
            plt.close()

        return int(prediction)

