import time
import numpy as np

from ocp_modules.controllers.ControllerBase import ControllerBase


class Lqr (ControllerBase):
    """Linear Quadratic Regulator

    The LQR exploits a special case of optimal control problems: If the cost function is
    quadratic and the model linear an optimal solution can be found for all initial states.
    Consequentially this solution can be computed offline (i.e. in advance), since we don't have
    to wait for the current state to wander by to compute the optimal control law at this point.

    There are four different variations of the core LQR formulation: finite-horizon
    time-continuous, infinite-horizon time-continuous, finite-horizon time-discrete and
    infinite-horizon time-discrete.

    The fourth variant is of interest, because real systems usually run for an unspecified /
    potentially unlimited time (infinite horizon) and are implemented on a sampling system
    (time-discrete).
    """

    def __init__(self, A, B, Q, R):
        self.K = Lqr.solveRiccati(A, B, Q, R)

    @staticmethod
    def solveRiccati(A, B, Q, R, eps=1e-6, timeOut=1.):
        # initialize P with Q
        P = Q

        # iterate over riccati equation to find P
        startTime = time.time()
        count = 0
        while True:
            Pnext = A.T @ P @ A - (A.T @ P @ B) \
                @ np.linalg.inv(R + B.T @ P @ B) \
                @ (B.T @ P @ A) + Q

            count += 1

            if np.isnan(Pnext).any():
                raise RuntimeError('NaN in Pnext after %d iterations' % count)

            # if timeout or changes smaller than <eps>, stop
            if time.time() - startTime > timeOut:
                print('solveRiccati(): timeout (%fs) after %d iterations' %
                      (timeOut, count))
                break
            elif (np.abs(P - Pnext) < eps).all():
                print(
                    'solveRiccati(): threshold (%f) reached after %d iterations' % (eps, count))
                break
            else:
                P = Pnext

        # compute the gain matrix
        K = np.linalg.inv(R + B.T @ P @ B) @ (B.T @ P @ A)

        return K

    def step(self, x0, xRefs, uRefs):
        """step Performs a control step taking the current state (x0) and a reference trajectory
        (xRefs, uRefs) and returns the controls for the current time step.

        :param x0: Current state (estimate)
        :param xRefs: Matrix where colums are reference states (LQR uses only the first state)
        :param uRefs: Matrix where colums are reference controls (LQR uses only the first control)
        :returns A 2-tuple (u, dict), where u are the resulting controls and dict a dictionary
        with metadata
        """
        u = - np.reshape(self.K @ np.reshape(x0 -
                                             xRefs[:, 0], (-1, 1)), (-1,)) + uRefs[:, 0]
        return u, {'f': None}
