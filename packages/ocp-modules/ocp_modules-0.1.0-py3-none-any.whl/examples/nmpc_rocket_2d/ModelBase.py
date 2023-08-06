from abc import ABC, abstractmethod

import casadi as ca
import numpy as np

from ocp_modules.utils.runge_kutta_4 import rk4step

class ModelBase(ABC):

    @staticmethod
    def createTimeDiscreteFun(ode, stepSize, NX, NU, integratorType='rk'):
        x = ca.SX.sym('x', NX)
        u = ca.SX.sym('u', NU)
        modelProps = {'x': x, 'p': u, 'ode': ode(x, u)}

        if integratorType == 'rk':
            return ca.Function('intg', [x,u], [rk4step(ode,x,u,stepSize)])
        else:
            return lambda x0, u: ca.integrator('intg', integratorType, modelProps, {'tf': stepSize})(x0=x0, p=u)['xf']

    @staticmethod
    def createPerturbedTimeDiscreteFun(ode, stepSize, NX, NU, integratorType='rk'):
        x = ca.SX.sym('x', NX)
        u = ca.SX.sym('u', NU)
        v = ca.SX.sym('v', NX)

        modelProps = {'x': x, 'p': u, 'ode': ode(x, u)}

        if integratorType == 'rk':
            return ca.Function('intg', [x,u,v], [rk4step(ode,x+v,u,stepSize)])
        else:
            return lambda x0, u, v: ca.integrator('intg', integratorType, modelProps, {'tf': stepSize})(x0=x0+v, p=u)['xf']

    @staticmethod
    def createTimeContFun(ode, NX, NU):
        x = ca.SX.sym('x', NX)
        u = ca.SX.sym('u', NU)
        return ca.Function('timeContFun', [x, u], [ode(x,u)])


    @staticmethod
    @abstractmethod
    def getNeutralState():
        pass

    def getDiscreteLinearSystem(self, ode, xLin, uLin, samplingTime):
        if ~hasattr(self, 'dfdx') or ~hasattr(self, 'dfdu'):
            NX = xLin.size
            NU = uLin.size
            x = ca.SX.sym('x', NX)
            u = ca.SX.sym('u', NU)
            self.dfdx = np.array(ca.Function('dfdx', [x,u], [ca.jacobian(ode(x,u), x)])(xLin, uLin))
            self.dfdu = np.array(ca.Function('dfdu', [x,u], [ca.jacobian(ode(x,u), u)])(xLin, uLin))

        A = np.eye(NX) + self.dfdx * samplingTime
        B = self.dfdu * samplingTime
        return (A, B)

    @classmethod
    def NUMSTATES(cls):
        return len(cls.stateLabels)

    @classmethod
    def NUMCONTROLS(cls):
        return len(cls.controlLabels)
