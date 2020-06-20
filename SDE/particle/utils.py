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