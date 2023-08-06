import numpy as np
from casadi import *
import tempfile
import os

def getCompiledSolver(solver, solver_opts):
    """getCompiledSolver Compiles a casadi nlpsol object into a shared library
    and returns a new solver object based on this binary.

    :param solver: Solver object to compile
    :param solver_opts: Compiled solver object
    """

    filename = 'casadi_solver_' + next(tempfile._get_candidate_names())
    solver.generate_dependencies(filename + '.c')

    print('Compiling NLP into %s.so...this might take a while' % filename)
    compile_flag = os.system('gcc -fPIC -shared %s.c -o /tmp/%s.so' % (filename, filename))

    os.remove(filename + '.c')

    return nlpsol('solver', 'ipopt', '/tmp/%s.so' % filename, solver_opts)
