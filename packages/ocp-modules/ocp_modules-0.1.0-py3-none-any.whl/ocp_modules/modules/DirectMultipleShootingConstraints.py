import numpy as np
from casadi import *
from casadi.tools import struct_symSX, entry

def gen(ocpVars, modelFun, M):
    """gen Generates the cosistency constraints emerging from applying
    direct multiple shooting to the prediction horizon discretization problem.

    :param ocpVars: A casadi struct_symSX object with fields x and u of correct size
    :param modelFun: A function defining a continuous-time dynamic model as an ODE. Must be evaluatable symbolically.
    :param M: Prediction horizon length

    :returns: A list of 3-tuples where each 3-tuple has the form <(symbolic constraint expression, lower bound, upper bound)>
    """

    constrList = []

    for i in range(M):
        x_k = ocpVars['x'][:,i]
        x_knext = ocpVars['x'][:,i+1]
        u_k = ocpVars['u'][:,i]

        # integrate for one time step
        x_sim = modelFun(x_k, u_k)

        # integration has to land on the start of next block
        g = x_knext - x_sim
        lbg = np.zeros(g.shape)
        ubg = np.zeros(g.shape)

        # create constraint tuple
        constrList += [(g, lbg, ubg)]

    return constrList
