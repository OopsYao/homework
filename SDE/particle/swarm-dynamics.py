from utils import delta_matrix, norm
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from progressbar import progressbar
import anikit
from utils import expand
import seaborn as sns

N = 800
T = 100
dt = T / anikit.FRAMES
g = .025 # Gravity


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


def evolve(t, barr_type=None):
    global Xt, x, v
    # Bessel process
    # Xt += dB[t] + dt / (2 * Xt)
    # Brownian motion
    Xt += dB[t]
    x += v * dt

    r = delta_matrix(x)
    r_norm = np.expand_dims(norm(r), axis=-1)

    with np.errstate(divide='ignore', invalid='ignore'):
        v = np.nansum(F(r_norm) / r_norm * r, axis=1) / N + (0, -g) + Xt / 15

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


fig, ax = plt.subplots()
ax.axis('off')
fig.tight_layout()
camera = Camera(fig)
for t in progressbar(range(anikit.FRAMES)):
    evolve(t, 'absorbing')
    ax.plot([-1, 1], [barrier, barrier])
    # ax.quiver(*(x.T), *(v.T) / 100, color='black', width=.003)
    ax.scatter(*(x.T), color='black')
    camera.snap()

# ax.quiver(*(x.T), *(v.T) / 100, color='black', width=.003)
animation = camera.animate(interval=2)
on_barrier = barrier_dist(x)
dist_plot(on_barrier)
plt.show()
# animation.save('particle/swarm/absorbing.mp4', fps=anikit.FPS, dpi=200)
