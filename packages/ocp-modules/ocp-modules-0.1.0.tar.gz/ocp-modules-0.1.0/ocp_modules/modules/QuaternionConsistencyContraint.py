import numpy as np
import casadi as ca
from casadi.tools import struct_symSX, entry


def gen(ocpVars):
    constrList = []
    M = ocpVars['u'].shape[1]

    for i in range(M):
        quat = ocpVars['u'][1:5, i]

        # norm has to be one
        g = ca.sumsqr(quat) - 1
        lbg = np.zeros(g.shape)
        ubg = np.zeros(g.shape)

        # create constraint tuple
        constrList += [(g, lbg, ubg)]

    return constrList