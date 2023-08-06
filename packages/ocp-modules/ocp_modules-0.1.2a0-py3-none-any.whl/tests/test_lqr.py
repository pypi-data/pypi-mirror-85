import numpy as np
from ocp_modules.controllers.Lqr import Lqr


def test_riccati():
    A = np.eye(2)
    B = np.eye(2)
    Q = np.eye(2)
    R = np.eye(2)

    K = Lqr.solveRiccati(A, B, Q, R)

    K_comparison = np.eye(2) * 0.6180339631667066  # MAGIC NUMBER

    assert np.allclose(K, K_comparison)


def test_step():
    A = np.eye(2)
    B = np.eye(2)
    Q = np.eye(2)
    R = np.eye(2)
    x = np.zeros((2,))
    x_ref = np.zeros((2, 1))
    u_ref = np.zeros((2, 1))

    lqr = Lqr(A, B, Q, R)
    u, data = lqr.step(x, x_ref, u_ref)

    assert np.allclose(u, np.zeros((2,)))
    assert data['f'] is None
