from utils import delta_matrix, norm
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from progressbar import progressbar
from anikit import FrameKit, ShootPlot
from utils import expand, vector_rescale
import seaborn as sns
from scipy.stats import norm as sci_norm

BARR = None


N = 800
T = 31
g = .1  # Gravity
mu = .05  # Random scale parameter
a = 1


def init():
    global frakit, dt, dB
    frakit = FrameKit(T)
    dt = frakit.dt
    dB = np.random.randn(int(T / dt), N, 2) * (dt ** .5)
    dB = np.vstack((np.tile(0, (1, N, 2)), dB))


def F(r, a=1, n=2):
    return a / r ** (n - 1) - r


# Initial [-1, 1] x [-1, 1]
x = 2 * np.random.rand(N, 2) - np.tile(1, (N, 2))
v = 0

barrier = -1.1
gate = 0
eps = 0.05
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


def evolve(f):
    global x, v

    x += v * dt

    r = delta_matrix(x)
    r_norm = expand(norm(r))

    # social force in v
    with np.errstate(divide='ignore', invalid='ignore'):
        v = np.nansum(F(r_norm) / r_norm * r, axis=1) / N
        if BARR != None:
            v += get_repulsion(x, 'fire' if 'gate' in BARR else 'gravity')

    dx = v * dt + mu * dB[f]
    # Fix barr velocity (to fix the position)
    if BARR != None:
        # if vertical position is around barrier
        x_next = x + dx
        # Invalid: cross the barrier
        # invalid = (x_next[:, 1] < barrier) ^ (x[:, 1] < barrier)
        # barrier with eps (vague judgement, not so strict)
        pr = x[:, 1]
        nx = x_next[:, 1]
        invalid = (pr > barrier) & (nx < barrier + eps)
        invalid |= (pr < barrier) & (nx > barrier - eps)

        if 'absorb' in BARR:
            # Absorbing barrier
            dx *= ~ expand(invalid)
        else:
            # Reflecting barrier
            if 'gate' in BARR:
                # Exclude those via gate: if before or after are within gate
                exclude = (np.abs(x_next[:, 0] - gate) < gate_len /
                           2) | (np.abs(x[:, 0] - gate) < gate_len / 2)
                invalid &= ~ exclude
            bdd = np.hstack((np.tile(False, (N, 1)), expand(invalid)))
            # v = np.where(bdd, -4 * v, v)
            dx = np.where(bdd, - dx, dx)

    # This is the real velocity at time t (contain social force and random term, i.e., dx = v * dt)
    v = dx / dt


sp = ShootPlot()
VIDEO_MODE = True
shoot = [0, 10, 20, 30, 40, 50, 100, 400, 1000, 5000]


def draw_barr(ax):
    if BARR != None:
        xmin, xmax = ax.get_xlim()
        if 'gate' in BARR:
            ax.plot([xmin, gate - gate_len / 2], [barrier, barrier],
                    color='blue', label='barrier')
            ax.plot([gate + gate_len / 2, xmax],
                    [barrier, barrier], color='blue')
        else:
            ax.plot([xmin, xmax], [barrier, barrier],
                    color='blue', label='barrier')

        # ax.legend(loc='upper right')


def trial():
    init()
    for f in progressbar(range(frakit.frames)):
        evolve(f)

        t = f * dt

        if VIDEO_MODE:
            sp.scatter(x)
            sp.text('t=%.2f' % t)
            # draw_barr(sp.ax)
            # xmin, xmax = sp.ax.get_xlim()
            if BARR != None:
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
                        f'particle/swarm/{BARR}-mu={mu}.a={a}.T={T}.t={s}.pdf')
                    sp.clear()

    else:
        if BARR == 'absorbing' and t == 50:
            plt.figure()
            on_barrier = barrier_dist(x)
            dist_plot(on_barrier)
            plt.savefig(
                f'particle/swarm/barrier-dist.mu={mu}.t={t}.pdf')

    if VIDEO_MODE:
        ani = sp.animate()
        ani.save(
            f'particle/swarm/{BARR}-mu={mu}.a={a}.T={T}.mp4', fps=frakit.FPS, dpi=200)


if __name__ == '__main__':
    BARR = 'absorbing'
    mu = 0.05
    # mu = 0
    T = 20
    a = 1
    VIDEO_MODE = True
    print(f'mu={mu}, a={a}, T={T}, {BARR} barrier')
    trial()
