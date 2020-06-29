from utils import delta_matrix, norm
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from progressbar import progressbar
from anikit import FrameKit, ShootPlot
from utils import expand, vector_rescale
import seaborn as sns

N = 800
T = 201
frakit = FrameKit(T, 10)
dt = frakit.dt
g = .5  # Gravity


def F(r, n=2):
    return 1 / r ** (n - 1) - r


# Initial [-1, 1] x [-1, 1]
x = 2 * np.random.rand(N, 2) - np.tile(1, (N, 2))
v = 0
dB = np.random.randn(int(T / dt), N, 2) * (dt ** .5)
# Stochastic process initial value
Xt = np.tile(.1, (N, 2))

barrier = -1.1
gate = 0
eps = 0.03


def barrier_dist(x):
    bdd = np.abs(x - barrier) < [0, eps]
    bdd = expand(bdd.sum(axis=-1))
    # [[nan, nan], [x, barrier], ...]
    y = np.where(bdd, x, np.nan)[:, 0]
    dist = y[~np.isnan(y)]
    return dist


def dist_plot(x):
    plt.figure()
    sns.distplot(x, hist=False, kde=True, bins=int(180/5), rug=True)


def evolve(f, barr_type=None):
    global Xt, x, v
    # Bessel process
    # Xt += dB[f] + dt / (2 * Xt)
    # Brownian motion
    Xt += dB[f]
    x += v * dt

    r = delta_matrix(x)
    r_norm = expand(norm(r))

    with np.errstate(divide='ignore', invalid='ignore'):
        v = np.nansum(F(r_norm) / r_norm * r, axis=1) / N + (0, -g)

    if barr_type != None:
        # if vertical position is around barrier
        bdd = np.abs(x - barrier) < [-np.inf, eps]

        if barr_type == 'reflect':
            # Reflect barrier
            # Exclude those on gate
            ongate = expand(np.abs(x[:, 0] - gate) < .1)
            bdd = ~ongate & bdd
            v = np.where(bdd, -v, v)
        else:
            # Absorbing barrier
            v = np.where(expand(bdd[:, 1]), 0, v)


# fig, ax = plt.subplots()
# ax.axis('off')
# fig.tight_layout()
# camera = Camera(fig)

shoot = [0, 10, 20, 30, 40, 400]
for f in progressbar(range(frakit.frames)):
    evolve(f, 'absorbing')
    t = f * dt
    # ax.scatter(*(x.T), color='black')

    for s in shoot:
        if abs(t - s) < dt / 2:
            sp = ShootPlot()
            sp.text(f't={t}')
            ax = sp.ax
            ax.plot([-1, 1], [barrier, barrier], color='blue')
            ax.quiver(*(x.T), *(vector_rescale(v).T), color='black', scale=50)
            # plt.figure()
            # plt.scatter(*(x.T), color='black')
    # camera.snap()

# animation = camera.animate(interval=2)
# on_barrier = barrier_dist(x)
# dist_plot(on_barrier)
plt.show()
# animation.save('particle/swarm/absorbing.mp4', fps=frakit.FPS, dpi=200)
