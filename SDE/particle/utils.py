import numpy as np
from numpy import linalg as LA
import unittest
import numpy.testing as npt


def delta_matrix(x):
    """ Get delta along axis 0, xij = xj - xi """
    x = np.expand_dims(x, axis=0)
    return x - np.moveaxis(x, 0, 1)


def norm(matrix, p=1):
    # Norm along the last axis
    norm_matrix = LA.norm(matrix, axis=-1) ** p
    return np.expand_dims(norm_matrix, axis=-1)


def cos_matrix(x, y):
    xy = x @ y.T
    nor = norm(x) * (norm(y).T)
    return xy / nor


class TestSuite(unittest.TestCase):

    def test_theta(self):
        a = np.array([
            [-1, 1],
            [1, 3 ** .5]
        ])
        b = np.array([
            [3 ** .5, 1],
            [0, -1]
        ])

        cos = cos_matrix(a, b)
        asp = np.array([
            [7 / 12, 3 / 4],
            [1 / 6,  5 / 6]
        ]) * np.pi
        npt.assert_almost_equal(cos, np.cos(asp))

    def test_bound(self):
        x = np.array([
            [-3, 2],
            [-5.0004, 2],
            [0.5, 4.994],
            [0, 0.5]
        ])

        eps = 0.03
        # If at door: |x[0]| <= 1 and |x[1]| < eps
        door = np.expand_dims((np.abs(x - [0, 0]) < [1, eps]).prod(axis=1), -1)
        low = np.abs(x - [-5, 0]) < eps  # at lower bound
        upp = np.abs(x - [5, 5]) < eps  # at upper bound

        asp = np.array([
            [False, False],
            [True, False],
            [False, True],
            [False, False]
        ])
        bdd = (~ door) & (low | upp)

        npt.assert_equal(asp, bdd)


if __name__ == "__main__":
    unittest.main()
