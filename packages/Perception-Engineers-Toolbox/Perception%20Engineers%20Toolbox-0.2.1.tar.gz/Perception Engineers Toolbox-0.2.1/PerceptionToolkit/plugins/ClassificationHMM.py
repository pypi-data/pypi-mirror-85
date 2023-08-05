from PerceptionToolkit import Version
from PerceptionToolkit.PluginInterfaces import IClassificationPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovements import Fixation
from typing import Sequence, Dict, Any, Union
from pomegranate import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib import patches
from scipy.interpolate import UnivariateSpline
from pandas import DataFrame as df
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM


class ClassificationHMM(IClassificationPlugin):
    """
    Classification HMM
    This implements two ways of classifying a sample using HMM (Hidden Markov Models).

    https://link.springer.com/article/10.3758/s13428-017-0876-8
    One is the Variational approach in which the states are defined using Variational Approach (optimal number of
    Gaussian is determined by BIC) . A Gaussian HMM is trained on an observation to attain its HMM parameters (priors,
    transition matrix coefficients, Gaussian center coordinates (means) and Gaussian variance coefficients along the x
    and y axis. These are used to form a feature gaze which is normalized to unit standard deviation and zero mean.
    linear Discriminant Analysis is used for classification.
    TODO not very effective due to limitation of pomegranate might remove later in favor of the Bayesian Inference.

    https://www.sciencedirect.com/science/article/pii/S0042698914002004
    The other method is the probabilistic Bayesian Inference approach. Kmeans clustering is used to locate the potential
    targets in an image (built-in in Pomegranate). A Gaussian HMM is trained for each task using the Baum-Welch alg.
    and give a likelihood probability via Forward algorithm. The Bayes rule is then applied to the likelihood term and
    the task-model with the highest posterior probability is selected.

    Attributes:
        enable_sampling: allows for sampling the fixations accounting for duration
        sampling: sampling in milliseconds (prediction performs best at sampling value of 1)
        method: either "inverse_yarbus" or "LDA"
        states: number of components in the model
        detect_optimal_states: at the fitting stage, an extra step is made to test for posterior probabilities of each
            task-trained HMM for K = 2..10. The K that gives the maximum a posteriori will determine the number of
            components used for the HMM.
        max_K: maximum number of clusters to be tested
        min_K: minimum number of clusters to be tested
        priors: list of priors if any

        min_std: minimum STD for each HMM state
        std: STD size for each HMM state
    """

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 1)

    def __init__(self):
        super(ClassificationHMM, self).__init__()

        self.method: str = "inverse_yarbus"
        # self.visualize: str = ""

        # self.K_max: int = 4
        self.states: int = None

        self.detect_optimal_states = False
        self.min_K: int = 2
        self.max_K: int = 10
        self.min_iterations: int = 0
        self.priors: list = None
        self.std: int = None
        self.min_std: int = None
        self.enable_sampling: bool = True
        self.sampling: int = 50

        self.filtering: str = 'none'
        self.image_size: tuple = None
        # self.image_filepath: str = None
        self.contamination: float = .01

        # self.file_path: str = ''
        # self.file_name: str = 'xvaldata.txt'

        self.model = None
        self.clf = None

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        # self.K_max = parameters.get("K_max", self.K_max)
        self.enable_sampling = parameters.get("enable_sampling", self.enable_sampling)
        self.sampling = parameters.get("sampling", self.sampling)
        assert self.sampling >= 1
        # self.method = parameters.get("method", self.method)
        # assert self.method in ["inverse_yarbus", "LDA"]
        self.states = parameters.get("states", self.states)
        assert self.states is None or self.states >= 1
        self.detect_optimal_states = parameters.get("detect_optimal_states", self.detect_optimal_states)
        self.max_K = parameters.get("max_K", self.max_K)
        self.min_K = parameters.get("min_K", self.min_K)
        assert self.max_K >= self.min_K
        assert self.min_K >= 1
        self.priors = parameters.get("priors", self.priors)
        self.std = parameters.get("std", self.std)
        self.min_std = parameters.get("min_std", self.min_std)
        self.min_iterations = parameters.get("min_iterations", self.min_iterations)

        self.filtering = parameters.get("filtering", self.filtering)
        self.contamination = parameters.get("contamination", self.contamination)
        self.image_size = parameters.get("image_size", self.image_size)
        # self.image_filepath = parameters.get("image_filepath", self.image_filepath)

        assert self.filtering in ['none', 'manual', 'auto']
        assert self.filtering != 'manual' or self.image_size is not None

    # LDA
    def create_feature_vector(self, fixations) -> np.ndarray:
        # Model the data using Variational GMM (Bayesian Gaussian Mixture) to get the covariance and mean coefficients
        # as well as potentially the ideal # of HMM states K

        # Parameters
        n_components = self.find_best_k(fixations)

        X = [[f] for f in fixations]

        hmm = HiddenMarkovModel.from_samples(
            NormalDistribution
            , n_components=n_components
            , X=X
        )

        # g consists of the following for K_max= 3
        # - priors 3
        # - trans matrix 3 x 3
        # - Gaussian center coordinates 3 x 2
        # - Gaussian variance coefficients along x an y 3 x 2
        # Total length of g = 24

        # trans, emission = hmm.forward_backward(fixations)
        # trans_matrix = np.array([t[:-2] for t in trans[1:-1]])
        full_trans_matrix = hmm.dense_transition_matrix()
        trans_matrix = np.array([t[:-2] for t in full_trans_matrix[1:-1]])

        # is the prior just the uniform weight concentration in gmm?
        # or is it the initial probabilities of each states at the start-state as defined by HMM?
        priors = np.array(full_trans_matrix[0][:-2])
        # priors = np.array(trans[0][:-2])

        gaussian_centers = []
        gaussian_covars = []

        # sample = hmm.sample(length=1000)
        # print(fixations)
        # print(sample)

        # for each state, get the mean coordinates

        for s in hmm.states:
            if s.distribution is not None:
                for p in s.distribution:
                    gaussian_centers.append(p.parameters[0])
                    gaussian_covars.append(p.parameters[1])

        g_temp = np.array([
            priors
            , trans_matrix.flatten()
            , gaussian_covars
            , gaussian_centers
        ])

        g = np.array([item for subarr in g_temp for item in subarr])

        return g

    # LDA
    @staticmethod
    def standardize_features(X):
        # standardize features by removing mean and scaling to unit variance
        scaler = StandardScaler()
        scaler.fit(X)
        return scaler.transform(X)

    def process_scanpath(self, data: DataModel) -> np.ndarray:
        # Receives a scanpath (DataModel)
        # Extracts all the fixations

        fixations_centroid_duration = np.apply_along_axis(
            lambda f: [Fixation(data, f[1], f[2]).centroid, Fixation(data, f[1], f[2]).duration],
            1,
            data.fixations())

        fixes = []
        if self.enable_sampling:
            for f, d in fixations_centroid_duration:
                repeat = int(d / self.sampling)
                for _ in range(repeat):
                    fixes.append(f)
        else:
            fixes = [f for f, d in fixations_centroid_duration]

        fixes = np.array(fixes)

        return fixes

    # BAYESIAN
    def find_best_k(self, X, graphic=False, plot_cluster=True) -> int:
        # find the optimal number of clusters K using the maximum silhouette method
        scores = []
        # clusters = []
        # distorsions = []
        min_K = self.min_K
        max_K = self.max_K

        for n_clusters in range(min_K, max_K + 1):
            clusterer = KMeans(n_clusters=n_clusters)
            cluster_labels = clusterer.fit_predict(X)
            # distorsions.append(clusterer.inertia_)
            silhouette_avg = silhouette_score(X, cluster_labels)

            scores.append(silhouette_avg)
            # clusters.append(n_clusters)

        k_max_silhouette = min_K + np.argmax(scores)

        return k_max_silhouette

    def filter_outliers(self, X, method="auto"):
        # given a sample set of shape (-1,2)
        # mark each coordinates as in/outliers: 1 or -1
        # returns an outlier mask of 1's and -1's

        outlier_mask = []
        if method == 'auto':
            estimator = IsolationForest(contamination=self.contamination)
            # estimator = OneClassSVM(kernel='sigmoid', gamma='scale')

            estimator.fit(X)
            outlier_mask = estimator.predict(X)
        elif method == 'manual':
            assert self.image_size is not None, "Warning: Image Size is not set"
            outlier_mask = [1
                            if 0 <= x[0] <= self.image_size[1]
                            and 0 <= x[1] <= self.image_size[0] else -1
                            for x in X]

        outlier_mask = np.asarray(outlier_mask)

        return outlier_mask

    def train_hmm(self, task_specific_scanpaths, l):

        same_label_set = []

        if self.filtering in ['auto', 'manual']:
            same_label_set = np.asarray([i for sublist in task_specific_scanpaths for i in sublist])
            decider = self.filter_outliers(same_label_set, method=self.filtering)
            task_specific_scanpaths = [same_label_set[np.where(decider > 0)]]

        if self.detect_optimal_states:
            if len(same_label_set) == 0:
                same_label_set = np.asarray([i for sublist in task_specific_scanpaths for i in sublist])

            self.states = self.find_best_k(same_label_set, graphic=False)
            print("Finding best k for label= ", l, "... K ---> ", self.states)

        # train a HMM for each task. Save it in a dictionary assigned to its label. Retrain if nan detected.
        invalid = True
        counter_1 = 500
        counter_2 = self.max_K - self.min_K
        # increment_state = False if self.max_K - self.states < self.states - self.min_K else True
        adjust = -1 if self.max_K - self.states < self.states - self.min_K else 1
        while invalid:
            # HMM is retrained if it produces a nan
            # if HMM produces only nans after a certain point (when counter_1 reaches 0), self.state is readjusted w/in
            # values (min_K, max_K)
            # if readjusted HMM still produces nan after a certain point (counter_2 reaches 0), produces warning

            counter_1 -= 1
            if counter_1 < 0:
                counter_2 -= 1
                if counter_2 < 0:
                    print("Warning: Having trouble training the HMM with the given min/max K values. Consider readjusting"
                          "the values and try again. Hint: last K-value chosen = {}".format(self.states))
                counter_1 = 500
                new_state = self.states + adjust
                print("Readjusting HMM states from n={} to n={}".format(self.states, new_state))

                # clamp new_state to [min_K, max_K]
                self.states = max(self.min_K, min(new_state, self.max_K))

            self.clf[l] = HiddenMarkovModel.from_samples(
                NormalDistribution
                , n_components=self.states
                , X=task_specific_scanpaths
                , algorithm='baum-welch'

                , pseudocount=.1
                , use_pseudocount=True
                , edge_inertia=.1

                , min_iterations=self.min_iterations
            )

            sample = self.clf[l].sample(length=1)
            for state_sample in sample:
                if np.any(np.isnan(state_sample.flatten())):
                    # print("nan detected")
                    invalid = True if counter_2 >= 0 else False
                    break
                else:
                    invalid = False
                    print("No NaNs detected.")

        if self.std is not None:
            for s in self.clf[l].states:
                if s.distribution is not None:
                    for p in s.distribution:
                        p.parameters = [p.parameters[0], self.std]

        if self.min_std is not None:
            for s in self.clf[l].states:
                if s.distribution is not None:
                    for p in s.distribution:
                        p.parameters = [p.parameters[0], max(self.min_std, p.parameters[1])]

    def check_convert_priors(self):
        # checks for existence and converts priors to log probability. Use uniform distribution if no priors given.
        if self.priors is not None and len(self.priors) == len(self.clf):
            self.priors = [np.log(p) for p in self.priors]
        else:
            warning_text = "Warning: Number of priors does not match the number of detected labels. Using uniform" \
                           " distribution!" if self.priors is not None else "No priors detected. Using uniform" \
                                                                            " distribution."
            print(warning_text)
            # uniform distribution
            n = len(self.clf)
            self.priors = [np.log(1/n) for _ in self.clf]

    def calculate_observation_probability(self, likelihood_terms) -> float:
        assert self.clf is not None

        # calculate the probability of that observation (scanpath) ever occurring
        #  Σ P( Obs | task') * P( task' )    <--- task' ∈ Tasks

        # P(O|t) * P(t) = e^log(P(O|t)) * e^log(P(t)) = e ^ log(P(O|t)) + log(P(t))
        # l and p are in logarithmic forms
        summands = [l + p for l, p in zip(likelihood_terms, self.priors)]

        # the sigma part of the equation
        p_obs = np.logaddexp.accumulate(summands)[-1]

        return p_obs

    def calculate_likelihood_terms(self, fixations):
        # [P( Obs | task ) for task in Tasks] using a task-trained HMM for each task

        likelihoods = [(l, self.clf[l].log_probability(fixations)) for l in self.clf]
        tasks, likelihood_terms = zip(*likelihoods)

        # Replace NaNs with a very small number
        likelihood_terms = np.asarray(likelihood_terms)
        likelihood_terms[np.isnan(likelihood_terms)] = np.nan_to_num(np.NINF)

        return tasks, likelihood_terms

    def infer_bayes(self, likelihood_terms, p_obs):
        #       P( task | Obs ) =           likelihood_terms[task] * P ( task )
        #                         ----------------------------------------------
        #                                               p_obs

        posteriors = [l + p - p_obs for l, p in zip(likelihood_terms, self.priors)]

        return posteriors

    def fit(self, data: Sequence[DataModel]) -> None:
        # _testing = False

        X = []  # feature space containing gaze features
        y = []  # labels for each gaze
        stimulus = []

        if self.method == "LDA":
            # get sequence of scanpaths
            for d in data:
                # Extract all fixations from that scanpath
                fixes = self.process_scanpath(d)

                g = self.create_feature_vector(fixes)
                X.append(g)
                y.append(d.meta[DataModel.META.LABEL])

            X = np.asarray(X)
            y = np.asarray(y)

            # X = self.standardize_features(X)

            # linear discriminant analysis step
            self.clf = LinearDiscriminantAnalysis()
            # self.clf = QuadraticDiscriminantAnalysis()
            self.clf.fit(X, y)
        else:
            for d in data:
                fixes = self.process_scanpath(d)
                X.append(fixes)
                y.append(d.meta[DataModel.META.LABEL])
                stimulus.append(d.meta[DataModel.META.STIMULUS])

            X = np.asarray(X)
            y = np.asarray(y)
            print('Total trained scanpaths', len(X))
            print('Training Labels', y)

            self.clf = {}
            categorized_scanpaths = []

            # train each task-hmm
            for l in np.unique(y):
                task_specific_scanpaths = [x for (x, t) in zip(X, y) if t == l]
                categorized_scanpaths.append(task_specific_scanpaths) #scanpaths grouped by task (for visualization)
                self.train_hmm(task_specific_scanpaths, l)

    def predict(self, data: DataModel) -> int:
        fixes = self.process_scanpath(data)

        if self.method == 'LDA':
            g = self.create_feature_vector(fixes)
            p = self.clf.predict([g])

            print(self.clf.predict_proba([g]))
            data.metrics['prediction'] = int(p)
            prediction = p
            print('prediction', prediction)

        else:
            # inference done by applying Bayes rule to the likelihood term calculated by the forward algorithm
            # P(task|Obs) = P(Obs|task)P(task) / P(Obs)
            #       where P(Obs) = sum( P(Obs|task(1-7)) P(task(1-7)) <-- sum of the likelihoods of the observation occuring
            #                                                               given each task times probability of said task

            #       P( task | Obs ) =           P( Obs | task ) * P ( task )
            #                         ----------------------------------------------
            #                         Σ P( Obs | task') * P( task' )    <--- task' ∈ Tasks

            # In the paper this is based on, uniform distribution is used for priori task, making it a Maximum Likelihood
            # Estimation of the task. Here, priors can be added by the user, otherwise assume uniform distribution.

            # pass the scanpath to each task-specific HMM and return a list of tuples: ( task, P(O|HMM_task)  )
            #   NANs as a result of the log_probability of a sequence given a task-trained HMM signifies that the
            #   sequence is impossible to produce under said HMM: check forward() on NANs as result
            #       https://pomegranate.readthedocs.io/en/latest/HiddenMarkovModel.html#log-probability

            # likelihood_terms == [ P( O|HMM_task' ) for task' = task 1 ... N ]

            # add up all observations
            #   P(O) = sum(P(O|task)P(task) for task = 1..7)
            #   here, the probabilities are presented in log form: p = exp(log(p))
            #   Hence we use np.logaddexp to add each log_probabilities one by one without having to convert to normal
            #   form and losing data as a result.

            self.check_convert_priors()

            tasks, likelihood_terms = self.calculate_likelihood_terms(fixes)

            p_obs = self.calculate_observation_probability(likelihood_terms)

            posteriors = self.infer_bayes(likelihood_terms, p_obs)

            prediction = tasks[np.argmax(posteriors)]

            data.metrics['predictions'] = list(zip(tasks, posteriors))
            data.metrics['prediction'] = prediction

        return int(prediction)
