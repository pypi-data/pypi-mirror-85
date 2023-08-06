import numpy as np
import casadi as ca
import time
import xarray as xr

from ocp_modules.controllers.ControllerBase import ControllerBase


class Nmpc (ControllerBase):

    def __init__(self, ocpVars, lbw, ubw, ocpParams, ocpCosts, ocpConstr, NX, NU, M, w0=None, solvOpts={}):
        self.var = ocpVars
        self.params = ocpParams
        self.costs = sum(ocpCosts)
        self.g = ca.vertcat(*[c[0] for c in ocpConstr])
        self.lbg = ca.vertcat(*[c[1] for c in ocpConstr])
        self.ubg = ca.vertcat(*[c[2] for c in ocpConstr])
        self.lbw = lbw
        self.ubw = ubw

        if w0 is None:
            w0 = np.zeros((ocpVars.size,))
        self.w0 = w0

        self.NX = NX
        self.NU = NU
        self.M = M

        if not solvOpts:
            solvOpts = {'ipopt': {'print_level': 1, 'linear_solver': 'mumps',
                                  'warm_start_entire_iterate': 'yes'}, 'print_time': 0}

        nlp = {'x': self.var, 'f': self.costs, 'g': self.g, 'p': self.params}

        self.solver = ca.nlpsol('solver', 'ipopt', nlp, solvOpts)

        self.solverResults = []
        self.durations = []

    def step(self, nlpParamValues, shift=True, reset_meta=False):
        if reset_meta:
            self.solverResults = []
            self.durations = []

        tick = time.time()
        res = self.solver(x0=self.w0, lbx=self.lbw, ubx=self.ubw,
                          lbg=self.lbg, ubg=self.ubg, p=nlpParamValues)
        dt = time.time() - tick

        # save result as initial guess for next iteration
        xsol = np.array(res['x'][:self.NX * (self.M + 1)])
        usol = np.array(res['x'][-self.NU * self.M:])
        if shift:
            self.w0 = np.concatenate(
                (xsol[self.NX:], xsol[-self.NX:], usol[self.NU:], usol[-self.NU:]))
        else:
            self.w0 = res['x']

        # save solver results
        self.solverResults.append(res)
        self.durations.append(dt)

        return np.reshape(usol, (self.NU, -1), order='F')

    def get_metadata(self) -> xr.Dataset:
        """Returns a xarray dataset containing artifact data of this class and its member classes

        Returns:
            xr.Dataset: A xarray.Dataset
        """

        meta = {}
        meta['controller_name'] = xr.DataArray('NMPC')
        meta['num_states'] = self.NX
        meta['num_controls'] = self.NU
        meta['horizon_length'] = self.M
        meta['residuals'] = xr.DataArray([float(res['f']) for res in self.solverResults],
                                         dims=('control_step'))
        if not self.solverResults:
            meta['solutions'] = xr.DataArray(np.zeros((1, 0)), dims=('solution', 'control_step'))
        else:
            solutions = np.array([np.asarray(res['x']).ravel() for res in self.solverResults],
                                 ndmin=2).T
            meta['solutions'] = xr.DataArray(solutions, dims=('solution', 'control_step'))
        # here one could also add lagrange multipliers to the dataset
        meta['computation_times'] = xr.DataArray(self.durations, dims=('control_step'))

        meta_dataset = xr.Dataset(data_vars=meta)

        return meta_dataset
