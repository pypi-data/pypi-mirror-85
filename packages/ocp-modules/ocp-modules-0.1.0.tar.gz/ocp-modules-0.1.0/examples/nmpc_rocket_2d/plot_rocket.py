import subprocess
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.gridspec as gridspec
from matplotlib.patches import Polygon
matplotlib.style.use('dark_background')

from ocp_modules.utils.mse import mse

def drawRocket(pos, ang, scale=1.0, ax=None, color='1.0'):
    if ax == None:
        ax = plt.gca()
    rotMtx = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    rocket = np.array([[0,0], [-1,-1], [2,0], [-1,1]]) * scale
    edges = np.apply_along_axis(lambda col: rotMtx @ col, 1, rocket) + pos
    p = Polygon(edges, facecolor='None', edgecolor=color)
    ax.add_patch(p)
    return p


def drawAstronaut(pos, scale=1.0, ax=None):
    if ax == None:
        ax = plt.gca()
    astroBody = np.array([[-1,-1.5], [-1.5,-2.0], [-1,-1.5], [1,-1.5], [1.5,-2.0], [1,-1.5],
        [1,1], [1.5,1.5], [1,1], [-1,1], [-1.5,1.5], [-1,1]]) * scale + pos
    p1 = Polygon(astroBody, facecolor='1.0', edgecolor='1.0')
    ax.add_patch(p1)

    astroHead = np.array([[-.8,1], [.8,1], [.8,2.6], [-.8,2.6]]) * scale + pos
    p2 = Polygon(astroHead, facecolor='0.0', edgecolor='1.0')
    ax.add_patch(p2)
    return p1, p2


def plotRocket(wSim, xRef=None, target=None, rocketColor='1.0'):
    if target == None:
        target = plt

    N = wSim.shape[1]

    ## plot rocket and astronaut
    for i in range(0,N):
        drawRocket(wSim[:2,i], wSim[4,i], 1.0, color=rocketColor)

    ## plot state and reference trajectories
    ax = target.plot(wSim[0,:],wSim[1,:], alpha=0.7)

    if type(xRef) == np.ndarray:
        # past references
        target.plot(xRef[0,:N],xRef[1,:N],'x--', alpha=0.7)

        # future references
        target.autoscale(False)
        target.plot(xRef[0,N-1:],xRef[1,N-1:],':', color='gray')

    plt.gca().set_aspect('equal', adjustable='box')


def plotRocketAndEva(wSim, xRef=None, target=None):
    if target == None:
        target = plt

    N = wSim.shape[1]

    ## plot rocket and astronaut
    for i in range(0,N):
        plt.plot(np.array([wSim[0,i], wSim[6,i]]), np.array([wSim[1,i], wSim[7,i]]), color='#333333')
        drawRocket(wSim[:2,i], wSim[4,i], 1.0)
        drawAstronaut(wSim[6:8,i], 0.8)

    ## plot state and reference trajectories
    target.plot(wSim[0,:],wSim[1,:], alpha=0.7)
    ax = target.plot(wSim[6,:],wSim[7,:], alpha=0.7)

    if type(xRef) == np.ndarray:
        # past references
        target.plot(xRef[0,:N],xRef[1,:N],'x--', alpha=0.7)
        target.plot(xRef[6,:N],xRef[7,:N],'x--', alpha=0.7)

        # future references
        target.autoscale(False)
        target.plot(xRef[0,N-1:],xRef[1,N-1:],':', color='gray')
        target.plot(xRef[6,N-1:],xRef[7,N-1:],':', color='gray')

        target.text(0.1, 0.9, "Pos.-MSE: %.3e" % mse(wSim[:2,:], xRef[:2,:N]),
          horizontalalignment='left',
          verticalalignment='center',
          transform = target.transAxes)

    plt.gca().set_aspect('equal', adjustable='box')


def plotControlSpace(u, target=None):
    if target == None:
        target = plt

    target.plot(u[1,:], u[0,:], 'd-')
    target.plot(u[1,0], u[0,0], 'x')
    #target.title = 'Control Space'


def renderToGif(w, ref=None, delay=10, filename='animation', plotAxes=True):
    print('Rendering to ' + filename + '.gif')
    N = w.shape[1]
    f, ax = plt.subplots()

    rocket, = ax.plot(w[0,:],w[1,:], alpha=0.5)
    astro, = ax.plot(w[6,:],w[7,:], alpha=0.5)
    if type(ref) is np.ndarray:
        refRocket, = ax.plot(ref[0,:N],ref[1,:N],'.--', alpha=0.7)
        refAstro, = ax.plot(ref[6,:N],ref[7,:N],'.--', alpha=0.7)
    ax.set_aspect('equal', adjustable='box')
    xLim = ax.get_xlim()
    yLim = ax.get_ylim()

    if not plotAxes:
        ax.set_axis_off()

    #def init():
    #    return rocket, astro, refRocket, refAstro

    def animate(i):
        if type(ref) is np.ndarray:
            text = ax.text(0.05, 1.1, "MSE: %.3e" % (mse(w[:2,:i], ref[:2,:i]) + mse(w[6:8,:i], ref[6:8,:i])),
              horizontalalignment='left',
              verticalalignment='bottom',
              transform = ax.transAxes,
              color=(0.7,0.7,0.7,0.5),
              weight='bold',
              size=35)
        rocket.set_data(w[:2,:i+1])
        astro.set_data(w[6:8,:i+1])
        #astro[0].set_data(w[6:8,:i])
        #refRocket[1].set_data(ref[:2,i])
        #refAstro[1].set_data(ref[6:8,i])
        r = drawRocket(w[:2,i], w[4,i], 2.0, ax)
        a1, a2 = drawAstronaut(w[6:8,i], 1.0, ax)
        tether, = ax.plot(np.array([w[0,i], w[6,i]]), np.array([w[1,i], w[7,i]]), color='#333333')
        ax.set_xlim(xLim)
        ax.set_ylim(yLim)
        return rocket, astro, r, a1, a2, tether, text

    for i in range(w.shape[1]):
        _,_,r,a1,a2,tether,text = animate(i)
        plt.savefig("./anim_{n:03d}.png".format(n=i), dpi=300, transparent=True,  frameon=False)
        r.remove()
        a1.remove()
        a2.remove()
        tether.remove()
        text.remove()

    args = ('convert -delay %i -loop 0 -dispose Background ./anim_*.png %s.gif' % (delay, filename)).split(' ')
    subprocess.call(args, shell=False)
    subprocess.call("rm ./anim_*.png", shell=True)

    #plt.show()
