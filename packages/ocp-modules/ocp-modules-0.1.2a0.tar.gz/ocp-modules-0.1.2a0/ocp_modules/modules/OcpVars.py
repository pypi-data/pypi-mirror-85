import numpy as np
import casadi as ca
from casadi.tools import struct_symSX, struct_SX, entry

def gen(NX, NU, M, stateBounds=None, controlBounds=None):
    """gen Generates a casadi struct containing the symbolic optimization variables required
    for direct multiple shooting. x is a <NX>x<M+1> matrix, u is a <NU>x<M> matrix.

    :param NX: Number of state variables
    :param NU: Number of control variables
    :param M: Prediction horizon length

    :returns: A casadi struct_symSX object
    """

    # decision (free) variables
    variables = struct_symSX([
        entry('x', shape=(NX,M+1)),
        entry('u', shape=(NU,M))])

    # symbolic bounds
    bx = ca.SX.sym('bx', NX)
    bu = ca.SX.sym('bu', NU)

    # bounds struct, must be identical to variables struct in dimensions and keys
    bounds = struct_SX([
        entry('x', expr=ca.repmat(bx, 1, M + 1)),
        entry('u', expr=ca.repmat(bu, 1, M))])
    boundsFun = ca.Function('varBoundsFun', [bx, bu], [bounds.cat])

    if stateBounds is None:
        stateBounds = np.multiply(np.ones((2,NX)), np.array((-np.inf, np.inf), ndmin=2).T)

    if controlBounds is None:
        controlBounds = np.multiply(np.ones((2,NU)), np.array((-np.inf, np.inf), ndmin=2).T)

    lbw = boundsFun(stateBounds[0,:], controlBounds[0,:])
    ubw = boundsFun(stateBounds[1,:], controlBounds[1,:])

    return variables, lbw, ubw
