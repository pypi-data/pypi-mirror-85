import numpy as np
from casadi import *
from casadi.tools import struct_symSX, entry

def gen(ocpVars, ocpParams):
    """gen Generates initial value constraints.

    :param ocpVars: A casadi struct_symSX object with field x of correct size
    :param ocpParams: A casadi struct_symSX object with field x_cur of correct size

    :returns: A list of 3-tuples where each 3-tuple has the form <(symbolic constraint expression, lower bound, upper bound)>
    """

    constrList = []

    # set current state as equality constraint
    g = ocpVars['x'][:,0] - ocpParams['x_cur']
    lbg = np.zeros(g.shape)
    ubg = np.zeros(g.shape)

    # create constraint tuple
    constrList += [(g, lbg, ubg)]

    return constrList
