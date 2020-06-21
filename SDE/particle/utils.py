import numpy as np
from numpy import linalg as LA


def delta_matrix(x):
    """ Get delta along axis 0, xij = xj - xi """
    x = np.expand_dims(x, axis=0)
    return x - np.moveaxis(x, 0, 1)


def norm(matrix, p=1):
    # Norm along the last axis
    norm_matrix = LA.norm(matrix, axis=-1) ** p
    return np.expand_dims(norm_matrix, axis=-1)


def theta_matrix(x, y):
    xy = x @ y.T
    nor = norm(x) * (norm(y).T)
    print(xy / nor)
    return np.arccos(xy / nor)


if __name__ == "__main__":
    x = np.array([[1, 2],
                  [-1, 1],
                  [2, 0.0002],
                  [-2, -2]])

    eps = 0.03
    # If at door: |x[0]| <= 1 and |x[1]| < eps
    door = np.expand_dims((np.abs(x - [0, 0]) < [1, eps]).prod(axis=1), -1)
    low = np.abs(x - [-5, 0]) < eps  # at lower bound
    upp = np.abs(x - [5, 5]) < eps  # at upper bound

    bdd = (~ door) & (low | upp)
    print(theta_matrix(x, x))
