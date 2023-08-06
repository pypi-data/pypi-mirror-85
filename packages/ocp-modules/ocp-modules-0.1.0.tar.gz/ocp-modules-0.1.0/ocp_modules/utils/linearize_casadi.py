import casadi as ca

def linearize_casadi(f,x,xLinPoint):
    """linearize_casadi Returns the first order approximation of a symbolic casadi expression.

    :param f: Function to be linearized
    :param x: Input variable of f
    :param xLinPoint: Linearization point
    """

    fLinFun = ca.Function('fLinFun', [x], [f])
    fJacFun = ca.Function('fJacFun', [x], [ca.jacobian(f,x)])
    return fLinFun(xLinPoint) + ca.mtimes(fJacFun(xLinPoint),(x - xLinPoint))



if __name__=='__main__':

    import casadi as ca
    import numpy as np
    import matplotlib.pyplot as plt

    x = ca.SX.sym('x')
    y = x*x*x / 2 - x*x - 1;
    xLinPoint = ca.SX.sym('xLinPoint')
    yLin = linearize_casadi(y,x,xLinPoint)

    yFun = ca.Function('yFun', [x], [y])
    yLinFun = ca.Function('yLinFun', [x, xLinPoint], [yLin])

    xSamples = np.arange(-2,2,0.1)
    ySamples = np.zeros_like(xSamples)
    yLinSamples = np.zeros((xSamples.size,xSamples.size))

    l = ['nl']
    for i,s in enumerate(np.linspace(-2,2,6)):
        l.append(str(s))
        for j,xs in enumerate(xSamples):
            yLinSamples[i,j] = yLinFun(xs, s)

    for i,s in enumerate(xSamples):
        ySamples[i] = yFun(s)


    plt.plot(xSamples, ySamples, ':')
    plt.autoscale(enable=False)
    plt.plot(xSamples, yLinSamples.T)
    plt.legend(l)
    plt.show()
