from unittest import TestCase
from PerceptionToolkit.plugins.ClassificationSubsMatch2 import *
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from itertools import permutations


class TestClassificationSubsMatch2(TestCase):
    def test_encode_data(self):
        self.run_encode_data([0, 0, 1, 1], [0, 0, 1, 1], 2)
        self.run_encode_data([0, 0, 1, 1], [0, 0, 1, 1], 2)
        self.run_encode_data([0, 0.5, 1], [0, 1, 2], 3)
        self.run_encode_data([0, 1, 2], [0, 1, 2], 3)

    def run_encode_data(self, test, expected_result, alphabet_size):
        subsmatch = ClassificationSubsMatch2()
        subsmatch.alphabet_size = alphabet_size
        encoded = subsmatch.encode_data(test)
        np.testing.assert_equal(encoded, expected_result)

    def test_encode(self):
        d = DataModel()
        d.raw = np.array([[0, 1, 2], [0, 1, 2], [0, 2, 1]])
        d.accessors[d.ET.LEFT_EYE_X] = 1
        d.accessors[d.ET.LEFT_EYE_Y] = 2
        d.accessors[d.ET.TIME] = 0

        d.events = np.array(
            [[EyeMovementTypes.FIXATION, 0, 0], [EyeMovementTypes.FIXATION, 1, 1], [EyeMovementTypes.FIXATION, 2, 2]])
        self.run_encode(d, [0, 1, 2], 3, 'percentile_horizontal')
        self.run_encode(d, [0, 2, 1], 3, 'percentile_vertical')
        self.run_encode(d, [0, 1, 2], 3, 'grid_horizontal')
        self.run_encode(d, [0, 0, 1], 2, 'grid_horizontal')
        d.raw[2, 2] = 10
        self.run_encode(d, [0, 0, 2], 3, 'grid_vertical')

    def run_encode(self, test, expected_result, alphabet_size, binning_method):
        subsmatch = ClassificationSubsMatch2()
        subsmatch.alphabet_size = alphabet_size
        subsmatch.binning_method = binning_method
        encoded = subsmatch.encode(test)
        np.testing.assert_equal(encoded, expected_result)

    def test_hash(self):
        # test individual hashes
        self.run_hash([0, 1, 2], 0 * pow(2, 0) + 1 * pow(2, 1) + 2 * pow(2, 2), 2)
        self.run_hash([0, 1, 2], 0 * pow(3, 0) + 1 * pow(3, 1) + 2 * pow(3, 2), 3)
        self.run_hash([5], 5 * pow(3, 0), 3)
        # test that there are no hash collisions happening
        perms = set(permutations([0, 1, 2, 3, 4]))
        subsmatch = ClassificationSubsMatch2()
        subsmatch.alphabet_size = 5
        seen_hashes = []
        for perm in perms:
            hash_val = subsmatch.hash(perm)
            self.assertTrue(hash_val not in seen_hashes)
            seen_hashes.append(hash_val)

    def run_hash(self, test, expected_result, alphabet_size):
        subsmatch = ClassificationSubsMatch2()
        subsmatch.alphabet_size = alphabet_size
        self.assertEqual(subsmatch.hash(test), expected_result)

    def test_split_n_grams(self):
        subsmatch = ClassificationSubsMatch2()
        subsmatch.n_gram_min = 2
        subsmatch.n_gram_max = 2
        ngrams = subsmatch.split_n_grams([0, 1, 1, 0])  # n-grams are: [0,1], [1,1], [1,0]
        expected = [subsmatch.hash([0, 1]), subsmatch.hash([1, 1]), subsmatch.hash([1, 0])]
        self.assertTrue(np.alltrue(ngrams == expected))

        # test merging of different n-gram lengths
        subsmatch.n_gram_min = 2
        subsmatch.n_gram_max = 3
        ngrams = subsmatch.split_n_grams([0, 1, 1, 0])  # n-grams are: [0,1], [1,1], [1,0], [0,1,1], [1,1,0]
        expected = [subsmatch.hash([0, 1]), subsmatch.hash([1, 1]), subsmatch.hash([1, 0]), subsmatch.hash([0, 1, 1]),
                    subsmatch.hash([1, 1, 0])]
        self.assertTrue(np.alltrue(ngrams == expected))

    def test_calculate_frequencies(self):
        subsmatch = ClassificationSubsMatch2()
        subsmatch.alphabet_size = 2
        subsmatch.n_gram_max = 2
        test = [0, 1]
        expectedResult = scipy.sparse.dok_matrix((pow(subsmatch.alphabet_size, subsmatch.n_gram_max),1), dtype=np.float64)
        expectedResult[0] = 0.5
        expectedResult[1] = 0.5
        self.assertTrue((subsmatch.calculate_frequencies(test) - expectedResult).sum() == 0)

        test = [0, 3]
        expectedResult = scipy.sparse.dok_matrix((pow(subsmatch.alphabet_size, subsmatch.n_gram_max),1), dtype=np.float64)
        expectedResult[0] = 0.5
        expectedResult[3] = 0.5
        self.assertTrue((subsmatch.calculate_frequencies(test) - expectedResult).sum() == 0)
