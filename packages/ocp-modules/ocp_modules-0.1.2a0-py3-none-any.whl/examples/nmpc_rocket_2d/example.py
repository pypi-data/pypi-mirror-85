#!/usr/bin/env python3

from ocp_modules.utils.mse import mse
from ocp_modules.controllers.Nmpc import Nmpc
from ocp_modules.modules import TrackingCosts
from ocp_modules.modules import DirectMultipleShootingConstraints, InitialValueConstraints
from ocp_modules.modules import OcpParams
from ocp_modules.modules import OcpVars
#from plot_rocket import plotRocket
from Rocket import Rocket as Model
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# constants
horizon_length = 20  # prediction horizon
sampling_time = 1e-1  # size of a step
control_limits = np.array([[0, -2e1], [2e3, 2e1]])  # maximum control value
state_weight = np.array([1., 1., 0., 0., 0., 0.1]) * 1e-2  # state weight
control_weight = np.array([0.01, 1.0]) * 1e-4  # control weight

dynamic_model = Model()
num_states = dynamic_model.NUMSTATES()
num_controls = dynamic_model.NUMCONTROLS()
dynamic_model_discrete = dynamic_model.createTimeDiscreteFun(dynamic_model.ode,
                                                             sampling_time,
                                                             num_states,
                                                             num_controls)

# expand weight parameters to full matrices
state_weight_matrix = np.kron(np.eye(horizon_length+1), np.diag(np.asarray(state_weight)))
control_weight_matrix = np.kron(np.eye(horizon_length), np.diag(np.asarray(control_weight)))

x0 = dynamic_model.getNeutralState()
u0 = np.zeros((4,))
w0 = np.hstack([np.tile(x0, [horizon_length + 1, ]), np.tile(u0, [horizon_length, ])])

# assemble controller
var, lbw, ubw = OcpVars.gen(
    num_states, num_controls, horizon_length, None, control_limits)
params = OcpParams.gen(num_states, num_controls, horizon_length)

costs = TrackingCosts.gen(var['x'][:], params['x_ref'][:], state_weight_matrix)
costs += TrackingCosts.gen(var['u'][:], params['u_ref']
                           [:], control_weight_matrix)

constr = InitialValueConstraints.gen(var, params)
constr += DirectMultipleShootingConstraints.gen(var,
                                                dynamic_model_discrete, horizon_length)

ctrl = Nmpc(var, lbw, ubw, params, costs, constr,
            num_states, num_controls, horizon_length)


# reference trajectory
Nsim = 50

w0 = np.array([-10.0, 0.0, 10, 0, 0, 0, 0, 0.1])
control_ref = np.zeros((num_controls, Nsim+horizon_length))
state_ref = np.zeros((num_states, Nsim+horizon_length+1))
np.random.seed(5)
state_ref[:2, :] = np.ones((2, Nsim+horizon_length+1)) * 100


# simulate
def simulation_function(x, u): return np.array(dynamic_model.createTimeDiscreteFun(
    dynamic_model.ode, sampling_time, num_states, num_controls)(x, u)).ravel()


def control_function(xCurLoc, xRefLoc, uRefLoc):
    param_value_map = {'x_cur': xCurLoc, 'x_ref': xRefLoc, 'u_ref': uRefLoc}
    ocp_param_values = OcpParams.fill(params, param_value_map)
    return ctrl.step(ocp_param_values)[:, 0]


wSim = np.zeros((num_states + num_controls, Nsim+1))
wSim[:num_states, 0] = x0

for i in range(Nsim):
    wSim[num_states:, i] = control_function(
        wSim[:num_states, i], state_ref[:, i], control_ref[:, i])

    wSim[:num_states, i +
         1] = simulation_function(wSim[:num_states, i], wSim[num_states:, i])


# Compute MSE for position
mseNlp = mse(wSim[:2, :], state_ref[:2, :-horizon_length])
print('NLP position MSE: %f' % mseNlp)

# plotting
t = np.arange(0, Nsim+1) * sampling_time
#plotRocket(wSim, state_ref, rocketColor='blue')
# plt.figure()
#plt.plot(wSim[0,:], wSim[1,:])
# plt.show()


plt.figure()
plt.subplot(4, 1, 1)
plt.plot(t, wSim[0:2, :].T)
plt.subplot(4, 1, 2)
plt.plot(t, wSim[2:4, :].T)
plt.subplot(4, 1, 3)
plt.plot(t, wSim[3, :].T)
plt.subplot(4, 1, 4)
plt.plot(t, wSim[4, :].T)
plt.show()
