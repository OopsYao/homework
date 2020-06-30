from utils import delta_matrix, norm
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from progressbar import progressbar
from anikit import FrameKit, ShootPlot
from utils import expand, vector_rescale
import seaborn as sns
from scipy.stats import norm as sci_norm

STO = False
BARR = None

print('sto' if STO else 'det', BARR)

N = 800
T = 401
frakit = FrameKit(T)
dt = frakit.dt
g = .1  # Gravity
mu = .05  # Random scale parameter


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
    bdd = np.abs(x - barrier) < [- np.inf, eps]
    bdd = expand(bdd[:, 1])
    # [[nan, nan], [x, barrier], ...]
    h = np.where(bdd, x, np.nan)[:, 0]
    # Drop nan
    dist = h[~np.isnan(h)]
    return dist


def dist_plot(x):
    plt.figure()
    sns.distplot(x, hist=False, kde=True, bins=int(
        180/5), rug=True, fit=sci_norm)


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
        v = np.nansum(F(r_norm) / r_norm * r, axis=1) / N
        if barr_type != None:
            v += (0, -g)
        if STO:
            v += mu * Xt

    if barr_type != None:
        # if vertical position is around barrier
        x_next = x + v * dt
        # Invalide: cross the barrier
        invalid = (x_next[:, 1] < barrier) ^ (x[:, 1] < barrier)

        if barr_type == 'absorbing':
            # Absorbing barrier
            v = np.where(expand(invalid), 0, v)
        else:
            # Reflecting barrier
            if barr_type == 'reflect-gate':
                # Exclude those via gate: if before or after are within gate
                exclude = (np.abs(x_next[:, 0] - gate)
                           < .1) | (np.abs(x[:, 0] - gate) < .1)
                invalid &= ~ exclude
            bdd = np.hstack((np.tile(False, (N, 1)), expand(invalid)))
            v = np.where(bdd, -v, v)


# fig, ax = plt.subplots()
# ax.axis('off')
# fig.tight_layout()
# camera = Camera(fig)
shoot = [0, 10, 20, 30, 40, 50, 100, 400, 1000, 5000]
for f in progressbar(range(frakit.frames)):
    evolve(f, BARR)

    t = f * dt

    for s in shoot:
        if abs(t - s) < dt / 2:
            sp = ShootPlot()
            sp.text(f't={t}')
            ax = sp.ax
            ax.quiver(*(x.T), *(vector_rescale(v).T),
                      color='black', scale=50, pivot='mid')

            if BARR != None:
                xmin, xmax = ax.get_xlim()
                if BARR == 'reflect-gate':
                    ax.plot([xmin, -.1], [barrier, barrier],
                            color='blue', label='barrier')
                    ax.plot([.1, xmax], [barrier, barrier], color='blue')
                else:
                    ax.plot([xmin, xmax], [barrier, barrier],
                            color='blue', label='barrier')
                ax.legend()

            ax.axis('off')
            ax.set_aspect('equal', 'box')
            sp.fig.savefig(
                f'particle/swarm/{"sto.mu=" + str(mu) if STO else "det"}{"-" + BARR + ".g=" + str(g) if BARR != None else ""}.t={s}.pdf')
    if abs(t - max(shoot)) < dt / 2 and BARR == 'absorbing':
        plt.figure()
        on_barrier = barrier_dist(x)
        dist_plot(on_barrier)
        plt.savefig(
            f'particle/swarm/{"sto.mu=" + str(mu) if STO else "det"}-barrier-dist.t={t}.pdf')

    # camera.snap()

# animation = camera.animate(interval=2)
# plt.show()
# animation.save('particle/swarm/absorbing.mp4', fps=frakit.FPS, dpi=200)
