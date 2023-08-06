import numpy as np

def mse(a,b):
    """mse Computes the mean square error (MSE) between two matrices of same shape.

    :param a: First matrix
    :param b: Second matrix
    """
    if a.shape != b.shape:
        raise RuntimeError("input arguments must have the same shape. supplied: %s, %s" % (a.shape, b.shape))
    return np.sum(np.power(a - b,2)) / a.size
