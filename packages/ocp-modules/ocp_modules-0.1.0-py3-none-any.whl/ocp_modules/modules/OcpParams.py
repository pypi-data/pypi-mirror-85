import numpy as np
import casadi as ca
from casadi.tools import struct_symSX, entry

def gen(NX, NU, M):
    """gen Generates a casadi struct containing the symbolic optimization parameters
    x_cur (the initial state), x_ref (the reference states) and u_cur (the reference controls).
    x_cur is a <NX>x<1> vector, x_ref is a <NX>x<M+1> matrix, u_ref is a <NU>x<M> matrix

    :param NX: Number of reference state variables
    :param NU: Number of reference control variables
    :param M: Prediction horizon length

    :returns: A casadi struct_symSX object
    """

    params = struct_symSX([
        entry('x_cur', shape=NX),
        entry('x_ref', shape=(NX,M+1)),
        entry('u_ref', shape=(NU,M))])

    return params

def fill(params, valueMap):
    paramFun = ca.Function('paramFun', [params[key] for key in valueMap.keys()], [params.cat])
    try:
        valueVec = np.array(paramFun(*valueMap.values())).ravel()
    except RuntimeError as re:
        print('Failed to fill values into parameter struct')
        print('Value dimensions: %s' % str([(k,v.shape) for k,v in valueMap.items()]))
        print('Struct dimensions: %s' % str([(e.name,e.dict['shape']) for e in params.entries]))
        raise re

    return valueVec
