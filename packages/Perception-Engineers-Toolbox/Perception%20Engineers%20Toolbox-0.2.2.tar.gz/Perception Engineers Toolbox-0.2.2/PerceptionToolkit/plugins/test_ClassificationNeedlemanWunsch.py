from unittest import TestCase, main
from PerceptionToolkit.plugins.ClassificationNeedlemanWunsch import *
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes


class TestClassificationNeedlemanWunsch(TestCase):
    def test_encode_fixation(self):
        # Test Image:
        #   0           5           10
        # 0 _________________________
        #   |   ROI_0   |   ROI_1   |
        # 5 -------------------------
        #   |   ROI_2   |   ROI_3   |
        # 10-------------------------

        needle = ClassificationNeedlemanWunsch()
        needle.image_dimensions = (10, 10)
        needle.vertical_alphabet_size = 2
        needle.horizontal_alphabet_size = 2

        fixation = [(0, 0), 100]
        fixation_2 = [(0, 6), 100]
        fixation_3 = [(6, 0), 100]
        fixation_4 = [(10, 10), 100]

        needle.encoding_boundaries_x = np.linspace(0, needle.image_dimensions[0], needle.horizontal_alphabet_size + 1)[1:]
        needle.encoding_boundaries_y = np.linspace(0, needle.image_dimensions[1], needle.vertical_alphabet_size + 1)[1:]

        # checking for disabled duration
        needle.enable_duration = False
        encoded_fix = needle.encode_fixation(fixation)
        encoded_fix_2 = needle.encode_fixation(fixation_2)
        encoded_fix_3 = needle.encode_fixation(fixation_3)
        encoded_fix_4 = needle.encode_fixation(fixation_4)

        self.assertEqual(encoded_fix, [0])
        self.assertEqual(encoded_fix_2, [2])
        self.assertEqual(encoded_fix_3, [1])
        self.assertEqual(encoded_fix_4, [3])

        # checking for enabled duration
        needle.enable_duration = True
        needle.sampling = 50
        encoded_fix = needle.encode_fixation(fixation)
        encoded_fix_2 = needle.encode_fixation(fixation_2)
        encoded_fix_3 = needle.encode_fixation(fixation_3)
        encoded_fix_4 = needle.encode_fixation(fixation_4)

        self.assertEqual(encoded_fix, [0, 0])
        self.assertEqual(encoded_fix_2, [2, 2])
        self.assertEqual(encoded_fix_3, [1, 1])
        self.assertEqual(encoded_fix_4, [3, 3])

    def generate_dm(self, raw):
        d = DataModel()
        d.raw = raw
        d.accessors[d.ET.LEFT_EYE_X] = 1
        d.accessors[d.ET.LEFT_EYE_Y] = 2
        d.accessors[d.ET.TIME] = 0

        d.events = np.array([
            [EyeMovementTypes.FIXATION, 0, 0],
            [EyeMovementTypes.FIXATION, 1, 1],
            [EyeMovementTypes.FIXATION, 2, 2],
            [EyeMovementTypes.FIXATION, 3, 3]
        ])
        return d

    def test_encode(self):
        # building a DataModel
        d = self.generate_dm(raw=np.array([
            [0, 100, 200, 300],
            [0, 6, 0, 10],
            [0, 0, 6, 10]
        ]))

        needle = ClassificationNeedlemanWunsch()
        needle.image_dimensions = (10, 10)
        needle.vertical_alphabet_size = 2
        needle.horizontal_alphabet_size = 2

        needle.find_boundaries([d])

        # checking for disabled duration
        needle.enable_duration = False
        needle.sampling = 20
        scanpath = needle.encode(d)
        self.assertEqual(scanpath, [0, 1, 2, 3])

        # checking for enabled duration
        needle.enable_duration = True
        needle.sampling = 20
        scanpath = needle.encode(d)
        self.assertEqual(scanpath, [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])

    # def test_align(self):
    #     score_mat = np.array([[0, 0, 0], [0, 1, 1], [0, 1, 0]])
    #     score_mat2 = np.array([[0, -2, -4], [-2, 1, -1], [-4, -1, -3]])
    #
    #     needle = ClassificationNeedlemanWunsch()
    #     needle.calculate_substitution_matrix(2)
    #
    #     needle.gap_penalty = 0
    #     needle.align(score_mat, [0,1], [0, 0])

    def test_compare_needlemanwunsch(self):
        scanpath_1 = [0, 0, 0, 0]
        scanpath_2 = [0, 0, 1, 1]
        scanpath_3 = [1, 1, 1, 1]

        needle = ClassificationNeedlemanWunsch()
        needle.horizontal_alphabet_size=2
        needle.vertical_alphabet_size=2
        needle.calculate_substitution_matrix(4)

        score_one = needle.compare_needlemanwunsch(scanpath_1, scanpath_1)
        score_half = needle.compare_needlemanwunsch(scanpath_1, scanpath_2)
        score_zero = needle.compare_needlemanwunsch(scanpath_1, scanpath_3)
        self.assertEqual(score_one, 1)
        self.assertEqual(score_half, 0.5)
        self.assertEqual(score_zero, 0)

    def test_get_match_score(self):
        scanpath_1 = [0, 0]
        scanpath_2 = [0, 1]

        needle = ClassificationNeedlemanWunsch()
        needle.vertical_alphabet_size = 2
        needle.horizontal_alphabet_size = 2
        needle.calculate_substitution_matrix(4)

        match = needle.get_match_score(0, 0, scanpath_1, scanpath_2)
        mismatch = needle.get_match_score(1, 1, scanpath_1, scanpath_2)

        self.assertEqual(match, 1)
        self.assertEqual(mismatch, -1)

    def test_get_score(self):
        score_mat = np.zeros((2, 2))
        score_mat[-1,-1] = 2

        sp_1 = [0, 0]
        sp_2 = [1, 1]

        needle = ClassificationNeedlemanWunsch()
        needle.horizontal_alphabet_size = 2
        needle.vertical_alphabet_size = 2
        subsmat = needle.calculate_substitution_matrix(4)
        print(subsmat)

        # score = needle.get_score(score_mat, sp_1, sp_2)
        # self.assertEqual(score, 1)

    def test_find_boundaries(self):
        min_x = 1
        min_y = 2
        max_x = 1111
        max_y = 2222
        d1 = self.generate_dm(raw=np.array([
            [0, 100, 200, 300],
            [min_x, 100, 100, 100],
            [100, 100, 100, 100]
        ]))
        d2 = self.generate_dm(raw=np.array([
            [0, 100, 200, 300],
            [100, 100, 100, max_x],
            [100, 100, 100, min_y]
        ]))
        d3 = self.generate_dm(raw=np.array([
            [0, 100, 200, 300],
            [100, 100, 100, 100],
            [100, max_y, 100, 100]
        ]))

        needle = ClassificationNeedlemanWunsch()
        t_minx, t_miny, t_maxx, t_maxy = needle.find_boundaries([d1, d2, d3])
        self.assertEqual(min_x, t_minx)
        self.assertEqual(min_y, t_miny)
        self.assertEqual(max_x, t_maxx)
        self.assertEqual(max_y, t_maxy)

        self.assertTrue(all([needle.encoding_boundaries_x[i] ==
                             np.linspace(min_x, max_x, needle.horizontal_alphabet_size + 1)[1:][i] for
                             i in range(needle.horizontal_alphabet_size)]))
        self.assertTrue(all([needle.encoding_boundaries_y[i] ==
                             np.linspace(min_y, max_y, needle.vertical_alphabet_size + 1)[1:][i] for i
                             in range(needle.vertical_alphabet_size)]))


if __name__ == '__main__':
    main()


