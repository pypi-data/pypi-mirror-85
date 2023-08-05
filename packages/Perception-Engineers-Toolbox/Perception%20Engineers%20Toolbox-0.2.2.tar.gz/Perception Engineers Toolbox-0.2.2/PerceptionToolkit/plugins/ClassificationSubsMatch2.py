from PerceptionToolkit.PluginInterfaces import IClassificationPlugin
from PerceptionToolkit.DataModel import DataModel
from typing import Sequence, Dict, Any, Union
from sklearn import svm
import numpy as np
from collections import Counter
from PerceptionToolkit.EyeMovements import Fixation
from PerceptionToolkit.Version import Version
import scipy.sparse

from sklearn.model_selection import cross_val_score


class ClassificationSubsMatch2(IClassificationPlugin):
    """
    SubsMatch 2.0
    Matches subsequence frequencies using a linear SVM
    https://www.hci.uni-tuebingen.de/assets/pdf/publications/TCUWE072016.pdf

    Attributes:
        n_gram_min: minimal length of nGrams to use
        n_gram_max: maximal length of nGrams to use
        alphabet_size: number of unique letters that make up the alphabet used for encoding. Larger alphabets correspond
            to more unique bins (there is no reason to limit this to 26, as we encode them as integers).
        binning_method: how to encode fixation sequences to letter sequences. Any of
            ["percentile_horizontal", "percentile_vertical", "grid_horizontal", "grid_vertical"]
    """

    def __init__(self):
        super(ClassificationSubsMatch2, self).__init__()
        self.n_gram_min: int = 2
        self.n_gram_max: int = 3
        self.alphabet_size: int = 5
        self.binning_method: str = "percentile_horizontal"
        self.linear_svm: Union[svm.LinearSVC, svm.NuSVC, svm.SVC, None] = None

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.n_gram_min = parameters.get("n_gram_min", self.n_gram_min)
        assert self.n_gram_min >= 1
        self.n_gram_max = parameters.get("n_gram_max", self.n_gram_max)
        assert self.n_gram_max >= self.n_gram_min
        self.alphabet_size = parameters.get("alphabet_size", self.alphabet_size)
        self.binning_method = parameters.get("binning_method", self.binning_method)
        assert self.binning_method in ["percentile_horizontal", "percentile_vertical", "grid_horizontal", "grid_vertical"]

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 1)

    def encode_data(self, data: Sequence[float]) -> Sequence[int]:
        encoding_boundaries = []
        if "percentile" in self.binning_method:
            encoding_boundaries = np.percentile(data, np.linspace(0, 100, self.alphabet_size + 1))[1:]
        if "grid" in self.binning_method:
            encoding_boundaries = np.linspace(min(data), max(data), self.alphabet_size + 1)[1:]
        # Split by encoding_boundaries
        encoding = np.zeros(len(data))
        for i, val in enumerate(data):
            encoding[i] = np.argmax(val <= encoding_boundaries)

        return encoding

    def encode(self, data: DataModel) -> Sequence[int]:
        # Find out whether we want to encode x or y
        relevant_dimension = []
        fixation_centroids = np.apply_along_axis(lambda f: Fixation(data, f[1], f[2]).centroid, 1, data.fixations())
        if "horizontal" in self.binning_method:
            relevant_dimension = fixation_centroids[:, 0]
        if "vertical" in self.binning_method:
            relevant_dimension = fixation_centroids[:, 1]

        return self.encode_data(relevant_dimension)

    def hash(self, n_gram: Sequence[int]) -> int:
        assert len(n_gram) > 0
        hash_value = 0
        for i, val in enumerate(n_gram):
            hash_value += val * pow(self.alphabet_size, i)
        return hash_value

    # returns a sequence of n_gram hashes
    def split_n_grams(self, data: Sequence[int]) -> Sequence[int]:
        hashed_n_grams = []
        for n_gram_length in range(self.n_gram_min, self.n_gram_max + 1):
            for i in range(0, len(data) - n_gram_length + 1):
                n_gram = data[i:(i + n_gram_length)]
                hashed_n_grams.append(self.hash(n_gram))
        return hashed_n_grams

    def calculate_frequencies(self, data: Sequence[int]) -> scipy.sparse.dok_matrix:
        res = Counter(data)
        total = sum(res.values())
        mat = scipy.sparse.dok_matrix((pow(self.alphabet_size, self.n_gram_max), 1), dtype=np.float64)
        for key in res:
            mat[key] = float(res[key]) / total
        return mat

    def fit(self, data: Sequence[DataModel]) -> None:
        # construct a sparse feature matrix
        features = []
        labels = []
        for scanpath in data:
            features.append(self.calculate_frequencies(self.split_n_grams(self.encode(scanpath))))
            labels.append(scanpath.meta[DataModel.META.LABEL])
        features = scipy.sparse.hstack(features)
        # Feature selection could be done here, e.g. via  sklearn.feature_selection.SelectKBest(chi2, k=2).fit_transform(X, y)
        # convert labels to categorical
        self.linear_svm = svm.LinearSVC()
        # self.linear_svm = svm.SVC(kernel="linear")
        # self.linear_svm = svm.NuSVC(kernel="linear")

        # Cross validation
        scores = cross_val_score(self.linear_svm, features.transpose(), labels, cv=5)
        # Train on all data
        # self.linear_svm.fit(features.transpose(), labels)
        print("Accuracy: %0.2f (+/- %0.2f) for SVM with %i classes (ngrams %i-%i, alphabet %i)." % (scores.mean(), scores.std() * 2, len(set(labels)), self.n_gram_min, self.n_gram_max, self.alphabet_size))

    def predict(self, data: DataModel) -> int:
        assert not (self.linear_svm is None)
        features = self.calculate_frequencies(self.split_n_grams(self.encode(data)))
        features = features.transpose()
        prediction = self.linear_svm.predict(features)
        print("SVM predicted %s" % (prediction[0]))
        return prediction[0]
