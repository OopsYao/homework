import numpy as np
import matplotlib.pyplot as plt
from progressbar import progressbar
from celluloid import Camera
from utils import delta_matrix, norm, expand
from anikit import FrameKit, ShootPlot
from forcelib import Morse, hyper_tang

D = 2  # Dimension
N = 400  # Number of prey
# N2 = 1

# Randomly initial distribution
x = 2 * np.random.rand(N, D)
# z = np.random.rand(N2, D)
z = np.array([
    [-0.1, 0.5],
    [2.1, 0.7],
    [-0.1, 0.3],
])
N2 = len(z)

T = 21
frakit = FrameKit(T, 6)
dt = frakit.dt

# fig, ax = plt.subplots()
# ax.axis('off')
# ax.set_aspect('equal', 'box')
# fig.tight_layout()
sp = ShootPlot()
camera = Camera(sp.fig)


c = 10
VIDEO_MODE = True
DRY_RUN = False


def prey_social(r):
    a = 1
    with np.errstate(divide='ignore', invalid='ignore'):
        return 1 / r - a * r
    # return Morse(r, 1, 1, .1, 1)


def prey_predator(r):
    # b = 0.2
    # q = 2
    # return N2 * b / (r ** (q - 1))
    return N2 * hyper_tang(r, 1, 1.5) / 2


def predator_social(r):
    # return 0
    # return Morse(r, 1, 1, .1, 1)
    return hyper_tang(r, 1, .7)


def predator_prey(r):
    # p = 3
    # return - c / (r ** (p - 1))
    return - c * hyper_tang(r, 1, 1)


z_trace = [z[0]]
v_trace = []
t_series = []
for f in progressbar(range(frakit.frames)):
    t = f * dt

    xx = delta_matrix(x)
    xx_norm = expand(norm(xx))

    zz = delta_matrix(z)
    zz_norm = expand(norm(zz))

    xz = delta_matrix(x, z)
    zx = - np.moveaxis(xz, 0, 1)

    xz_norm = norm(xz)
    zx_norm = xz_norm.T
    xz_norm = expand(xz_norm)
    zx_norm = expand(zx_norm)

    with np.errstate(divide='ignore', invalid='ignore'):
        vx = np.nansum(prey_social(xx_norm) / xx_norm * xx, 1) / N + \
            np.nansum(prey_predator(xz_norm) / xz_norm * xz, 1) / N2
        vz = np.nansum(predator_social(zz_norm) / zz_norm * zz, 1) / N2 + \
            np.nansum(predator_prey(zx_norm) / zx_norm * zx, 1) / N

    if not DRY_RUN:
        if VIDEO_MODE:
            # sp.ax.scatter(*(x.T), color='black')
            # sp.ax.scatter(*(z.T), color='red')
            sp.scatter(x, color='black')
            sp.scatter(z, color='red')
            sp.text('t=%.2f' % t)
            camera.snap()
        else:
            for s in range(T):
                if abs(t - s) < dt / 2:
                    sp.quiver(x, vx)
                    sp.quiver(z, vz, color='blue')
                    sp.ax.axis('off')
                    sp.ax.set_aspect('equal', 'box')
                    sp.text('t=%.2f' % t)
                    sp.fig.savefig(
                        f'particle/prey/tanh-two-predator.c={c}.t={t}.pdf')
                    sp.ax.cla()

    v_trace.append(vz[0])

    x += vx * dt
    z += vz * dt
    t_series.append(t)
    z_trace.append(z[0])

if VIDEO_MODE:
    animation = camera.animate()
    animation.save(
        f'particle/prey/two-prey-pradator{c}.mp4', fps=frakit.FPS, dpi=200)

if DRY_RUN:
    z_trace = np.array(z_trace)
    v_trace = np.array(v_trace)
    plt.figure()
    # plt.plot(t, z_trace[:, 0], label='horizontal')
    # plt.plot(t, z_trace[:, 1], label='vertical')
    plt.plot(t_series, v_trace[:, 0], label='horizontal')
    plt.plot(t_series, v_trace[:, 1], label='vertical')
    plt.ylabel('v')
    plt.xlabel('t')
    plt.legend()
    plt.show()
