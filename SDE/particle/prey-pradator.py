import numpy as np
import matplotlib.pyplot as plt
from progressbar import progressbar
from celluloid import Camera
from utils import delta_matrix, norm, expand
from anikit import FrameKit, ShootPlot
from forcelib import Morse, hyper_tang

D = 2  # Dimension
N = 400  # Number of prey
N2 = 3

# Randomly initial distribution
x = 2 * np.random.rand(N, D)
# z = np.random.rand(N2, D)
z = np.array([
    [-0.1, 0.5],
    [2.1, 0.7],
    [-0.1, 0.3],
])

T = 41
frakit = FrameKit(T)
dt = frakit.dt

fig, ax = plt.subplots()
ax.axis('off')
fig.tight_layout()
camera = Camera(fig)
sp = ShootPlot()


c = .8


def tanh_force(r):
    a = 10
    b = .1
    return np.tanh(a * (1 - r)) + b


def prey_social(r):
    a = 1
    with np.errstate(divide='ignore', invalid='ignore'):
        return 1 / r - a * r
    # return tanh_force(r)


def prey_predator(r):
    # b = 0.2
    # q = 2
    # return N2 * b / (r ** (q - 1))
    return N2 * Morse(r, 1, 1, .1, 1)


def predator_social(r):
    return 0


def predator_prey(r):
    # p = 3
    # return - c / (r ** (p - 1))
    return - c * hyper_tang(r, 1, 1)


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

    for s in range(T):
        if abs(t - s) < dt / 2:
            sp.quiver(x, vx)
            sp.quiver(z, vz, color='blue')
            sp.ax.axis('off')
            sp.ax.set_aspect('equal', 'box')
            sp.text('t=%.2f' % t)
            sp.fig.savefig(f'particle/prey/c={c}.t={t}.pdf')
            sp.ax.cla()

    # camera.snap()
    x += vx * dt
    z += vz * dt

# animation = camera.animate()
# plt.show()
# animation.save(f'particle/prey/prey-pradator{c}.mp4', fps=frakit.FPS, dpi=200)
