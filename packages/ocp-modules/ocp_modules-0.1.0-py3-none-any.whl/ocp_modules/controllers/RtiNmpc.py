import numpy as np
import casadi as ca
import xarray as xr
import time

from ocp_modules.controllers.ControllerBase import ControllerBase
from ocp_modules.utils.linearize_casadi import linearize_casadi as linearize


class RtiNmpc (ControllerBase):

    def __init__(self, ocpVars, lbw, ubw, ocpParams, ocpCosts, ocpConstr, NX, NU, M, w0, Q, R, solvOpts={}):
        self.var = ocpVars
        self.lbw = lbw
        self.ubw = ubw
        self.params = ocpParams
        self.costs = sum(ocpCosts)
        self.g = ca.vertcat(*[c[0] for c in ocpConstr])
        self.lbg = ca.vertcat(*[c[1] for c in ocpConstr])
        self.ubg = ca.vertcat(*[c[2] for c in ocpConstr])
        self.w0 = w0
        self.lagrMulConstr = np.zeros((self.g.numel(),))
        self.lagrMulOptVars = np.zeros((self.var.cat.numel(),))

        self.NX = NX
        self.NU = NU
        self.M = M

        # symbolic variables
        w = ca.vertcat(self.var['x'][:], self.var['u']
                       [:])  # primal decision variables
        # constraint lagrange multipliers (lambda + mu, i.e. dual decision variables)
        lagrMult = ca.SX.sym('lagrMult', self.g.size())
        wGuess = ca.SX.sym('wGuess', w.shape)  # guess / linearization point

        # single weight matrix for all decision variables
        W = np.diag(np.concatenate([np.tile(Q, M+1), np.tile(R, M)]))

        L = self.costs + lagrMult.T @ self.g
        B = ca.Function('B', [w], [ca.hessian(L,w)[0]])(wGuess)

        wErr = w - wGuess
        # reference as QP parameters
        wRef = ca.vertcat(self.params['x_ref'][:], self.params['u_ref'][:])

        #B = W  # gauss-newton hessian approximation
        J = W @ (wGuess - wRef)

        fqp = 1./2. * wErr.T @ B @ wErr + J.T @ wErr
        gqp = linearize(self.g, w, wGuess)
        pqp = ca.vertcat(self.params.cat, wGuess, lagrMult)

        # assemble QP
        if not solvOpts:
            solvOpts = {'jit': False, 'print_time': 0, 'printLevel': 'low',
                        'sparse': True, 'enableEqualities': True}
            #solvOpts = {'jit' : True, 'print_time' : 0, 'printLevel' : 'high', 'sparse' : True}

        qp = {'x': self.var, 'f': fqp, 'g': gqp, 'p': pqp}
        self.solver = ca.qpsol('S', 'qpoases', qp, solvOpts)

        self.solverResults = []
        self.durations = []

    def step(self, ocp_parameter_values):
        """Computes the solution to the configured OCP and returns the complete
        predicted control trajectory.

        Args:
            ocp_parameter_values (dict): Dictionary with keys that match the symbolic OCP
            parameters. The values are filled in according to the structure of the symbolic
            expression.

        Raises:
            RuntimeError: If the passed parameter values contain NaNs, this exception is raised

        Returns:
            numpy.ndarray: Returns a <number_controls>x<horizon_length> matrix containing the
            predicted controls
        """

        tick = time.time()

        # update initial guess with current state estimate
        self.w0[:self.NX] = ocp_parameter_values[:self.NX]

        # assemble ocp parameter vector
        extended_parameter_values = np.concatenate(
            [ocp_parameter_values, self.w0, self.lagrMulConstr])

        if any(np.isnan(extended_parameter_values)):
            raise RuntimeError("OCP parameters contain NaNs")

        # solve QP
        res = self.solver(x0=self.w0,
                          lbx=self.lbw,
                          ubx=self.ubw,
                          lbg=self.lbg,
                          ubg=self.ubg,
                          p=extended_parameter_values,
                          lam_x0=self.lagrMulOptVars,
                          lam_g0=self.lagrMulConstr)

        # stop time
        dt = time.time() - tick

        # save result as initial guess for next iteration
        self.lagrMulConstr = np.array(res['lam_g']).ravel()
        self.lagrMulOptVars = np.array(res['lam_x']).ravel()

        self.w0 = np.array(res['x']).ravel()

        # save meta data
        self.solverResults.append(res)
        self.durations.append(dt)

        return np.reshape(np.array(res['x'][-self.NU * self.M:]), (self.NU, -1), order='F')

    def get_metadata(self) -> xr.Dataset:
        """Returns a xarray dataset containing artifact data of this class and its member classes

        Returns:
            xr.Dataset: A xarray.Dataset
        """

        meta = {}
        meta['controller_name'] = xr.DataArray('RTI_NMPC')
        meta['num_states'] = self.NX
        meta['num_controls'] = self.NU
        meta['horizon_length'] = self.M
        meta['residuals'] = xr.DataArray([float(res['f']) for res in self.solverResults],
                                         dims=('control_step'))

        solution_state_data = np.zeros((self.NX, self.M+1, len(self.solverResults)))
        solution_control_data = np.zeros((self.NU, self.M, len(self.solverResults)))

        for i, res in enumerate(self.solverResults):
            solution_state_data[:,:,i] = np.reshape(res['x'][:self.NX * (self.M + 1)], (self.NX, self.M + 1), order='F')
            solution_control_data[:,:,i] = np.reshape(res['x'][-self.NU * self.M:], (self.NU, self.M), order='F')

        meta['solution_states'] = xr.DataArray(solution_state_data, dims=('state', 'control_state_horizon', 'control_step'))
        meta['solution_controls'] = xr.DataArray(solution_control_data, dims=('control', 'control_action_horizon', 'control_step'))

        # here one could also add lagrange multipliers to the dataset
        meta['computation_times'] = xr.DataArray(self.durations, dims=('control_step'))

        meta_dataset = xr.Dataset(data_vars=meta)

        return meta_dataset
