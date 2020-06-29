import numpy as np
from numpy import linalg as LA
import unittest
import numpy.testing as npt


def delta_matrix(x, y=None):
    """ Get delta along axis 0, zij = xi - yj """
    # 1 x N x D (1 x N if we view the last axis as a whole)
    if type(y) == type(None):
        y = x
    x = np.expand_dims(x, axis=0)
    y = np.expand_dims(y, axis=0)
    return np.moveaxis(x, 0, 1) - y


def norm(matrix, p=1):
    # Norm along the last axis
    norm_matrix = LA.norm(matrix, axis=-1) ** p
    return norm_matrix


def blind(v, x):
    v = np.expand_dims(v, axis=1)
    prod = (v * x).sum(axis=-1)
    return prod / (norm(v) * norm(x))


def expand(ndarray):
    return np.expand_dims(ndarray, axis=-1)


def vector_rescale(v):
    r = norm(v)
    with np.errstate(divide='ignore'):
        v = v * expand(np.log(1 + r) / r)
        return np.nan_to_num(v)

class TestSuite(unittest.TestCase):

    def test_delta_matrix(self):
        x = np.array([
            [1, 3],
            [3, 4],
            [-2, 1]
        ])
        y = np.array([
            [-1, 3],
            [2, 1]
        ])
        asp = np.array([
            [[2, 0], [-1, 2]],
            [[4, 1], [1, 3]],
            [[-1, -2], [-4, 0]]
        ])
        npt.assert_equal(asp, delta_matrix(x, y))

    def test_blind(self):
        v = np.array([
            [-1, 1],
            [1, 3 ** .5]
        ])
        x = np.array([
            [[0, 1], [1, -1], [1, 1]],
            [[3 ** .5, 1], [1, -1], [1, 0]]
        ])

        asp = np.array([
            [1 / 4, 1, 1 / 2],
            [1 / 6, 7 / 12, 1 / 3]
        ]) * np.pi
        npt.assert_almost_equal(blind(v, x), np.cos(asp))

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
