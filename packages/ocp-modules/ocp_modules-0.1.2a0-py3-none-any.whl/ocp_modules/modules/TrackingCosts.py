import numpy as np
import operator
from casadi import *
from casadi.tools import struct_symSX, entry

def gen(vecA, vecB, weightMatrix, errorFun=None):
    """gen Generates a cost expression based on the weighted quadratic error between the
    specified symbolic variables.

    :param vecA: Vector of symbolic variables
    :param vecB: Vector of symbolic variables
    :param weightMatrix: A matrix of size <size(vecA)>x<size(vecB)>
    :param errorFun: Allows to use a custom difference operator. If none (default), operator.sub is used.

    :returns: A list of cost expressions
    """

    if errorFun is None:
        errorFun = operator.sub
    errVec = errorFun(vecA, vecB)
    cost = mtimes(mtimes(errVec.T, weightMatrix), errVec)

    return [cost]
