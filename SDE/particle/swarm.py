import numpy as np
from utils import delta_matrix, norm, expand
from misc import snap_iter
from anikit import ShootPlot
import matplotlib.pyplot as plt
import seaborn as sns

# Types of barrier
NO_BARR = 'nobarr'
REFLECT = 'reflect'
ABSORB = 'absorb'
# Barrier location
BARR = - 1.1
# Rough barrier
EPS = .01

# Particle num
N = 800

barr_type = NO_BARR
a = 1
gate_len = 0
mu = 0


def F(r, a):
    return a / r - r


def system_generator(x0,  dt):
    x = x0
    t = 0
    dB = 0
    while True:
        xx = delta_matrix(x)
        r_xx = norm(xx, keepdims=True)

        # Interaction among individuals
        with np.errstate(divide='ignore', invalid='ignore'):
            v = np.nansum(F(r_xx, a) / r_xx * xx, axis=1) / N

        # Environment influence
        if barr_type != NO_BARR:
            # Add env
            if gate_len != 0:
                # Point repulsion
                c = (0, 1.5)
                xc = x - c
                v += .5 / norm(xc, keepdims=True) ** 2 * xc
            else:
                # Gravity
                v += (0, - .1)

        # dx without barrier consideration
        # Plus random diffusion
        dx = v * dt + mu * dB

        # Now consider different barrier
        if barr_type != NO_BARR:
            x_next = x + dx

            # barrier with EPS (vague judgement, not so strict)
            pr = x[:, 1]
            nx = x_next[:, 1]
            invalid = (pr > BARR) & (nx < BARR + EPS)  # Upper to lower
            invalid |= (pr < BARR) & (nx > BARR - EPS)  # Lower to upper

            if barr_type == ABSORB:
                dx *= ~ expand(invalid)
            else:
                # Reflecting barrier
                if gate_len != 0:
                    # Exclude those via gate: if before or after are within gate
                    exclude = (np.abs(x_next[:, 0] - 0) < gate_len /
                               2) | (np.abs(x[:, 0] - 0) < gate_len / 2)
                    invalid &= ~ exclude

                bdd = np.hstack((np.tile(False, (N, 1)), expand(invalid)))
                dx = np.where(bdd, - dx, dx)

        v = dx / dt
        yield t, x, v
        t += dt
        # Do not use +=, as it modifies the mutable variable x (by `__iadd__` method)
        x = x + dx
        if mu != 0:
            dB = np.random.randn(N, 2)


def draw_barr(ax):
    if barr_type != NO_BARR:
        xmin, xmax = ax.get_xlim()

        if gate_len != 0:
            ax.plot([xmin, 0 - gate_len / 2], [BARR, BARR],
                    color='blue', label='barrier')
            ax.plot([0 + gate_len / 2, xmax],
                    [BARR, BARR], color='blue')
        else:
            ax.plot([xmin, xmax], [BARR, BARR],
                    color='blue', label='barrier')


class NumCounter:
    def __init__(self):
        self._t_series = []
        self._r_series = []

    def _ratio_outside(self, x):
        return (x[:, 1] <= BARR).sum() / N

    def add(self, t, x):
        self._t_series.append(t)
        self._r_series.append(self._ratio_outside(x))

    def export(self):
        return self._t_series, self._r_series


def escape_ratio(gl, x0):
    # Escape ratio
    global gate_len, barr_type, mu
    mu = 0
    gate_len = gl
    barr_type = REFLECT
    counter = NumCounter()
    snap = np.linspace(0, 40, 2000)
    for t, x, _ in snap_iter(snap, system_generator(x0, dt), dt):
        counter.add(t, x)
    return counter.export()


def barrier_dist(x):
    bdd = np.abs(x[:, 1] - BARR) <= 2 * EPS
    bdd = expand(bdd)

    # e.g. [[nan, nan], [x_h, barrier], ...]
    h = np.where(bdd, x, np.nan)[:, 0]
    # Drop nan
    dist = h[~ np.isnan(h)]

    plt.figure()
    sns.distplot(dist, hist=False, kde=True, bins=int(180 / 5), rug=True)


if __name__ == '__main__':
    dt = .01

    # Initial [-1, 1] x [-1, 1]
    x0 = 2 * np.random.rand(N, 2) - np.tile(1, (N, 2))

    barr_type = REFLECT
    gate_len = 0.2

    mu = 0.05
    a = 1

    # watch = np.hstack((
    #     np.linspace(0, 3, 50),
    #     np.linspace(3, 20, 10),
    #     np.linspace(20, 100, 10),
    #     np.linspace(100, 800, 10),
    #     np.linspace(800, 1600, 10),
    # ))
    # jobname = f'{barr_type if barr_type == NO_BARR or gate_len == 0 else "gate=" + str(gate_len)}.mu={mu}.a={a}'
    # print(jobname)
    # sp = ShootPlot()
    # sp.fig.set_figheight(4)
    # sp.fig.set_figwidth(4)
    # sys_iter = system_generator(x0, dt)
    # for s, x, v in snap_iter(watch, sys_iter, dt):
    #     sp.quiver(x, v)
    #     draw_barr(sp.ax)
    #     sp.save(f'particle/swarm/{jobname}.t={s:.2f}.pdf')
    #     sp.clear()
    # else:
    #     if barr_type == ABSORB:
    #         barrier_dist(x)
    #         plt.savefig(f'particle/swarm/dist.mu={mu}.a={a}.t={s:.2f}.pdf')

    t1, r1 = escape_ratio(.1, x0)
    t2, r2 = escape_ratio(.2, x0)
    t3, r3 = escape_ratio(.4, x0)

    plt.figure()
    plt.plot(t1, r1, label='gate=0.1')
    plt.plot(t2, r2, label='gate=0.2')
    plt.plot(t3, r3, label='gate=0.4')
    plt.xlabel('t')
    plt.ylabel('r')
    plt.legend()
    plt.show()
