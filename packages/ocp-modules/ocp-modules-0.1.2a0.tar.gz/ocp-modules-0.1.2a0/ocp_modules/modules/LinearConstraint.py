import numpy as np
from casadi import *
from casadi.tools import struct_symSX, entry

def gen(var, A, lba, uba):

    g = A @ var
    constrList = [(g, lba, uba)]

    return constrList
