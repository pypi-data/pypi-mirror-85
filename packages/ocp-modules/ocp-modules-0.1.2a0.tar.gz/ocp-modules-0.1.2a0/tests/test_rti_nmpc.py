import numpy as np
import xarray as xr
from ocp_modules.controllers.RtiNmpc import RtiNmpc
from ocp_modules.modules import OcpVars
from ocp_modules.modules import OcpParams


def test_get_metadata():
    """Tests if the metadata creation works and is returned correctly.
    """

    horizon_length = 10
    num_states = 10
    num_controls = 4

    x0 = np.zeros((num_states,))
    u0 = np.zeros((4,))
    w0 = np.hstack([np.tile(x0, [horizon_length + 1, ]),
                    np.tile(u0, [horizon_length, ])])

    # assemble controller
    var, lbw, ubw = OcpVars.gen(num_states, num_controls, horizon_length, None, None)
    ocp_params = OcpParams.gen(num_states, num_controls, horizon_length)

    costs = [var['x'][0]]
    constraints = [(var['u'][0], -1, 1)]

    state_weight = np.ones((num_states,))
    control_weight = np.ones((num_controls,))

    controller = RtiNmpc(var, lbw, ubw, ocp_params, costs, constraints, num_states, num_controls,
                         horizon_length, w0, state_weight, control_weight)

    metadata = controller.get_metadata()

    # test static values
    assert type(metadata) is xr.Dataset
    assert metadata.controller_name == 'RTI_NMPC'

    assert metadata.num_states == num_states
    assert metadata.num_controls == num_controls
    assert metadata.horizon_length == horizon_length

    # test dynamic values before first iteration
    assert metadata.residuals.size == 0
    assert metadata.solution_states.size == 0
    assert metadata.solution_controls.size == 0

    # test dynamic values after first iteration
    parameter_values = {'x_cur': x0,
                        'x_ref': np.zeros((num_states, horizon_length+1)),
                        'u_ref': np.zeros((num_controls, horizon_length))}
    nlp_parameters = OcpParams.fill(ocp_params, parameter_values)
    controller.step(nlp_parameters)
    metadata = controller.get_metadata()
    assert metadata.residuals.shape == (1,)
    assert metadata.solution_states.shape == (num_states, horizon_length+1, 1)
    assert metadata.solution_controls.shape == (num_controls, horizon_length, 1)
    assert metadata.computation_times.shape == (1,)
