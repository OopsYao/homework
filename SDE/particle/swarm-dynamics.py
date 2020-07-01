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
BARR = 'absorbing'

print('sto' if STO else 'det', BARR)

N = 800
T = 31
frakit = FrameKit(T)
dt = frakit.dt
g = .1  # Gravity
mu = .05  # Random scale parameter
a = 1


def F(r, a=1, n=2):
    return a / r ** (n - 1) - r


# Initial [-1, 1] x [-1, 1]
x = 2 * np.random.rand(N, 2) - np.tile(1, (N, 2))
v = 0
dB = np.random.randn(int(T / dt), N, 2) * (dt ** .5)
dB = np.vstack((np.tile(0, (1, N, 2)), dB))
Bt = np.cumsum(dB, axis=0)
# Stochastic process initial value
Xt = np.tile(.1, (N, 2))

barrier = -1.1
gate = 0
eps = 0.03
gate_len = .2


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


def get_repulsion(x, form='gravity'):
    if form == 'gravity':
        return np.array([0, -g])
    else:
        c = (0, 1.5)
        xc = x - c
        return .5 / norm(xc, keepdims=True) ** 2 * xc


class NumCounter:
    def __init__(self):
        self._t_series = []
        self._n_series = []

    def _num_inside(self, x):
        return (x[:, 1] >= barrier).sum()

    def add(self, t, n):
        self._t_series.append(t)
        self._n_series.append(n)

    def export(self):
        return self._t_series, self._n_series


def evolve(f, barr_type=None):
    global Xt, x, v
    # Bessel process
    # Xt += dB[f] + dt / (2 * Xt)
    # Brownian motion
    x += v * dt
    if STO:
        x += mu * dB[f] * (v != 0)

    r = delta_matrix(x)
    r_norm = expand(norm(r))

    with np.errstate(divide='ignore', invalid='ignore'):
        v = np.nansum(F(r_norm) / r_norm * r, axis=1) / N
        if barr_type != None:
            v += get_repulsion(x, 'gravity')

    if barr_type != None:
        # if vertical position is around barrier
        x_next = x + v * dt
        # Invalid: cross the barrier
        invalid = (x_next[:, 1] < barrier) ^ (x[:, 1] < barrier)
        # # barrier with eps
        # pr = x[:, 1]
        # nx = x_next[:, 1]
        # invalid = (pr > barrier + eps) & (nx < barrier)
        # invalid |= (pr < barrier) & (nx > barrier)

        if barr_type == 'absorbing':
            # Absorbing barrier
            v = np.where(expand(invalid), 0, v)
        else:
            # Reflecting barrier
            if barr_type == 'reflect-gate':
                # Exclude those via gate: if before or after are within gate
                exclude = (np.abs(x_next[:, 0] - gate) < gate_len /
                           2) | (np.abs(x[:, 0] - gate) < gate_len / 2)
                invalid &= ~ exclude
            bdd = np.hstack((np.tile(False, (N, 1)), expand(invalid)))
            v = np.where(bdd, -4 * v, v)


sp = ShootPlot()
VIDEO_MODE = True
shoot = [0, 10, 20, 30, 40, 50, 100, 400, 1000, 5000]


def draw_barr(ax):
    if BARR != None:
        xmin, xmax = ax.get_xlim()
        if BARR == 'reflect-gate':
            ax.plot([xmin, gate - gate_len / 2], [barrier, barrier],
                    color='blue', label='barrier')
            ax.plot([gate + gate_len / 2, xmax],
                    [barrier, barrier], color='blue')
        else:
            ax.plot([xmin, xmax], [barrier, barrier],
                    color='blue', label='barrier')

        # ax.legend(loc='upper right')


for f in progressbar(range(frakit.frames)):
    evolve(f, BARR)

    t = f * dt

    if VIDEO_MODE:
        sp.scatter(x)
        sp.text('t=%.2f' % t)
        # draw_barr(sp.ax)
        # xmin, xmax = sp.ax.get_xlim()
        sp.ax.plot([-2, 2], [barrier, barrier],
                   color='blue', label='barrier')
        sp.snap()
    else:
        for s in shoot:
            if abs(t - s) < dt / 2:
                sp.text(f't={t}')
                sp.quiver(x, v)
                # draw_barr(sp.ax)
                sp.fig.savefig(
                    f'particle/swarm/{"sto.mu=" + str(mu) if STO else "det"}{"-" + BARR if BARR != None else ""}.t={s}.pdf')
                sp.clear()

else:
    if BARR == 'absorbing' and t == 50:
        plt.figure()
        on_barrier = barrier_dist(x)
        dist_plot(on_barrier)
        plt.savefig(
            f'particle/swarm/{"sto.mu=" + str(mu) if STO else "det"}-barrier-dist.t={t}.pdf')

if VIDEO_MODE:
    ani = sp.animate()
    ani.save(
        f'particle/swarm/{"sto.mu=" + str(mu) if STO else "det"}-{BARR}.a={a}.mp4', fps=frakit.FPS, dpi=200)
