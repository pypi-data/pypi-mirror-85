
def rk4step(ode, x, u, h):
    """rk4step Integrates an ODE using a Runge-Kutta 4 integrator

    :param ode: ODE
    :param x: initial state
    :param u: controls
    :param h: step size
    """

    k1 = ode(x, u)
    k2 = ode(x + (h / 2.0) * k1, u)
    k3 = ode(x + (h / 2.0) * k2, u)
    k4 = ode(x + h * k3, u)
    x_next = x + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    return x_next
