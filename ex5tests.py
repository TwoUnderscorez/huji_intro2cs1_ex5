import unittest
from typing import Any

import cartoonify as user


class CartoonifyTests(unittest.TestCase):
    MAX_DIFF_ALLOWED = 1
    EXPECTED_CHANGED_MSG = "You've changed the input matrix, which according to the PDF is ont allowed"

    def test__separate_channels__example_form_pdf(self):
        self.assertListEqual(
            [[[1]], [[2]]],
            user.separate_channels([[[1, 2]]]),
            'Example given on page 2'
        )

    def test__separate_channels__example_from_forum(self):
        self.assertListEqual(
            [[[1, 4], [7, 10]],
             [[2, 5], [8, 11]],
             [[3, 6], [9, 12]]],
            user.separate_channels(
                [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
            ),
            'Example from the forum: https://moodle2.cs.huji.ac.il/nu21/mod/forumng/discuss.php?d=2226&expand=1#p5642'
        )

    def test__combine_channels__example_from_pdf(self):
        input_ = [[[1]], [[2]]]
        self.assertListEqual(
            [[[1, 2]]],
            user.combine_channels(input_),
            'Example given on page 2'
        )

    def test__combine_channels__example_from_forum(self):
        self.assertListEqual(
            [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
            user.combine_channels(
                [[[1, 4], [7, 10]],
                 [[2, 5], [8, 11]],
                 [[3, 6], [9, 12]]]),
            'Example from the forum: https://moodle2.cs.huji.ac.il/nu21/mod/forumng/discuss.php?d=2226&expand=1#p5642'
        )

    def test__RGB2grayscale__example_from_pdf(self):
        input_ = [[[100, 180, 240]]]
        self.assertListEqual(
            [[163]],
            user.RGB2grayscale(input_),
            'Example given on page 3'
        )

    def test__blur_kernel__example_from_pdf(self):
        self.assertListEqual(
            [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]],
            user.blur_kernel(3),
            'Example given on page 3'
        )

    def test__apply_kernel__example_from_pdf(self):
        blur_kernel = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
        self.assertListEqual(
            [[14, 128, 241]],
            user.apply_kernel([[0, 128, 255]], blur_kernel),
            'Example given on page 3'
        )

    def test__bilinear_interpolation__example_from_pdf(self):
        image = [[0, 64], [128, 255]]
        self.assertAlmostEqual(
            0,
            user.bilinear_interpolation(image, 0, 0),
            msg='Example 1 of 4 given on page 4, delta is 1',
            delta=CartoonifyTests.MAX_DIFF_ALLOWED
        )
        self.assertAlmostEqual(
            255,
            user.bilinear_interpolation(image, 1, 1),
            msg='Example 2 of 4 given on page 4, delta is 1',
            delta=CartoonifyTests.MAX_DIFF_ALLOWED
        )
        self.assertAlmostEqual(
            112,
            user.bilinear_interpolation(image, 0.5, 0.5),
            msg='Example 3 of 4 given on page 4, delta is 1',
            delta=CartoonifyTests.MAX_DIFF_ALLOWED
        )
        self.assertAlmostEqual(
            160,
            user.bilinear_interpolation(image, 0.5, 1),
            msg='Example 4 of 4 given on page 4, delta is 1',
            delta=CartoonifyTests.MAX_DIFF_ALLOWED
        )

    def test__bilinear_interpolation__example_from_forum(self):
        self.assertAlmostEqual(
            4,
            user.bilinear_interpolation(
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0.5, 1.25),
            msg='Based on the images posted by TA Adi Ravid',
            delta=CartoonifyTests.MAX_DIFF_ALLOWED
        )

    def test__rotate_90__example_from_pdf(self):
        matrix = [[1, 2, 3], [4, 5, 6]]
        self.assertListEqual(
            [[4, 1], [5, 2], [6, 3]],
            user.rotate_90(matrix, 'R'),
            'Example 1/2 given on page 5'
        )
        self.assertListEqual(
            [[3, 6], [2, 5], [1, 4]],
            user.rotate_90(matrix, 'L'),
            'Example 2/2 given on page 5'
        )

    def test__get_edges__example_from_pdf(self):
        self.assertListEqual(
            [[255, 0, 255]],
            user.get_edges([[200, 50, 200]], 3, 3, 10),
            'Example given on page 6'
        )

    def test__quantize__example_from_pdf(self):
        self.assertListAlmostEqual(
            [[0, 32, 96], [128, 191, 223]],
            user.quantize([[0, 50, 100], [150, 200, 250]], 8),
            'Example given on page 7, delta is 1'
        )

    def test__quantize_colored_image__(self):
        pass

    def test__add_mask__example_from_pdf(self):
        self.assertListEqual(
            [[200, 125, 50]],
            user.add_mask([[50, 50, 50]], [[200, 200, 200]], [[0, 0.5, 1]]),
            'Example given on page 8'
        )

    def test__add_mask__accepts_colored_image(self):
        self.assertListEqual(
            [[[200, 200, 200], [125, 125, 125], [50, 50, 50]]],
            user.add_mask(
                [[[50, 50, 50], [50, 50, 50], [50, 50, 50]]],
                [[[200, 200, 200], [200, 200, 200], [200, 200, 200]]],
                [[0, 0.5, 1]]
            ),
            '''The instructions state that `add_mask` should be able to apply
            a mask both single-channel (2d matrix) images and on multi-channel
            (3d matrix) images (by separating the colored image to channels
            and applying the mask)
            Inspired by the example on page 9'''
        )

    def assertListAlmostEqual(self, a1, a2, delta=1, msg=None):
        self.assertTrue(
            CartoonifyTests._are_almost_equal(
                a1,
                a2,
                -1,
                delta
            ),
            msg
        )

    @ staticmethod
    def _are_almost_equal(o1: Any, o2: Any, max_abs_ratio_diff: float, max_abs_diff: float) -> bool:
        """
        Compares two objects by recursively walking them trough. Equality is as usual except for floats.
        Floats are compared according to the two measures defined below.

        :param o1: The first object.
        :param o2: The second object.
        :param max_abs_ratio_diff: The maximum allowed absolute value of the difference.
        `abs(1 - (o1 / o2)` and vice-versa if o2 == 0.0. Ignored if < 0.
        :param max_abs_diff: The maximum allowed absolute difference `abs(o1 - o2)`. Ignored if < 0.
        :return: Whether the two objects are almost equal.

        https://stackoverflow.com/questions/12136762/assertalmostequal-in-python-unit-test-for-collections-of-floats
        """
        if type(o1) != type(o2):
            return False

        composite_type_passed = False

        if hasattr(o1, '__slots__'):
            if len(o1.__slots__) != len(o2.__slots__):
                return False
            if any(not CartoonifyTests._are_almost_equal(getattr(o1, s1), getattr(o2, s2),
                                                         max_abs_ratio_diff, max_abs_diff)
                   for s1, s2 in zip(sorted(o1.__slots__), sorted(o2.__slots__))):
                return False
            else:
                composite_type_passed = True

        if hasattr(o1, '__dict__'):
            if len(o1.__dict__) != len(o2.__dict__):
                return False
            if any(not CartoonifyTests._are_almost_equal(k1, k2, max_abs_ratio_diff, max_abs_diff)
                   or not CartoonifyTests._are_almost_equal(v1, v2, max_abs_ratio_diff, max_abs_diff)
                   for ((k1, v1), (k2, v2))
                   in zip(sorted(o1.__dict__.items()), sorted(o2.__dict__.items()))
                   if not k1.startswith('__')):  # avoid infinite loops
                return False
            else:
                composite_type_passed = True

        if isinstance(o1, dict):
            if len(o1) != len(o2):
                return False
            if any(not CartoonifyTests._are_almost_equal(k1, k2, max_abs_ratio_diff, max_abs_diff)
                   or not CartoonifyTests._are_almost_equal(v1, v2, max_abs_ratio_diff, max_abs_diff)
                   for ((k1, v1), (k2, v2)) in zip(sorted(o1.items()), sorted(o2.items()))):
                return False

        elif any(issubclass(o1.__class__, c) for c in (list, tuple, set)):
            if len(o1) != len(o2):
                return False
            if any(not CartoonifyTests._are_almost_equal(v1, v2, max_abs_ratio_diff, max_abs_diff)
                   for v1, v2 in zip(o1, o2)):
                return False

        elif isinstance(o1, float):
            if o1 == o2:
                return True
            else:
                if max_abs_ratio_diff > 0:  # if max_abs_ratio_diff < 0, max_abs_ratio_diff is ignored
                    if o2 != 0:
                        if abs(1.0 - (o1 / o2)) > max_abs_ratio_diff:
                            return False
                    else:  # if both == 0, we already returned True
                        if abs(1.0 - (o2 / o1)) > max_abs_ratio_diff:
                            return False
                # if max_abs_diff < 0, max_abs_diff is ignored
                if 0 < max_abs_diff < abs(o1 - o2):
                    return False
                return True

        else:
            if not composite_type_passed:
                return o1 == o2

        return True


if __name__ == '__main__':
    unittest.main()
