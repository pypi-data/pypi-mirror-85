import casadi as ca

from ocp_modules.utils.quaternion import quaternionProduct as qProd
from ocp_modules.utils.runge_kutta_4 import rk4step
from ModelBase import ModelBase


# a 2D rocket with thrust and torque controls
class Rocket(ModelBase):
    stateLabels = ['px', 'py', 'vx', 'vy', 'phi', 'omega']
    controlLabels = ['f', 't']

    def __init__(self, params = None):
        self.params = {
                'mass': 1.0,
                'momOfInert': 1,
                'linearFriction': 0,
                'angularFriction': 0,
                }

        if (params):
            self.params.update(params)

    def ode(self, currentState, controls, externalForce = 0):
        v = currentState[2:4] # linear velocity
        phi = currentState[4] # angular velocity
        omega = currentState[5] # angular velocity

        f = controls[0] # external force
        t = controls[1] # external torque
        I = self.params['momOfInert'] # inertia tensor
        m = self.params['mass'] # mass
        muL = self.params['linearFriction']
        muA = self.params['angularFriction']

        pDot = v
        vDot = ca.vertcat(ca.cos(phi) * f / m, ca.sin(phi) * f / m) - muL * v + externalForce

        phiDot = omega
        omegaDot = t / I - muA * omega

        return ca.vertcat(pDot, vDot, phiDot, omegaDot)

    @staticmethod
    def getNeutralState():
        x0 = [0., 0., 0., 0., 0., 0.]
        return x0
