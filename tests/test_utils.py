__author__ = 'Nathan.Woodrow'

import unittest

import utils

class PointFunctionTests(unittest.TestCase):
    def test_pairs_returns_non_matching_tail_head(self):
        points = [1,2,3,4]
        pairs = utils.pairs(points, matchtail=False)
        one = next(pairs)
        two = next(pairs)
        self.assertNotEqual(one[1], two[0])

    def test_pairs_returns_matching_tail_head(self):
        points = [1,2,3,4]
        pairs = utils.pairs(points, matchtail=True)
        one = next(pairs)
        two = next(pairs)
        self.assertEqual(one[1], two[0])


if __name__ == '__main__':
    unittest.main()
