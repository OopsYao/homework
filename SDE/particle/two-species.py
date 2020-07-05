import numpy as np
from utils import delta_matrix, norm, expand
from progressbar import progressbar
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from celluloid import Camera
import anikit
from anikit import ShootPlot, FrameKit


def V_neg_prime(s):
    Cr, Ca = [1, 1]
    lr, la = [.1, 1]
    s = np.sqrt(2 * s)
    return Cr * np.exp(- s / lr) / (lr * s) - Ca * np.exp(- s / la) / (la * s)


a = [10, 10, 2]
b = [.1, .1, .3]


def g(s, i):
    ai = a[i - 1]
    bi = b[i - 1]
    s = np.sqrt(2 * s)
    with np.errstate(divide='ignore'):
        return (np.tanh(ai * (1 - s)) + bi) / s


N1 = 200
N2 = 200
mu = N2 / N1
T = 301
frakit = FrameKit(T)
dt = frakit.dt

x = np.random.rand(N1, 2)
y = np.random.rand(N2, 2)
# w, h = figaspect(1.)
# fig, ax = plt.subplots(figsize=(w, h))

# ax.axis('off')
# fig.tight_layout()
# camera = Camera(fig)

sp = ShootPlot()
for t in progressbar(range(frakit.frames)):
    mx = delta_matrix(x)
    my = delta_matrix(y)
    mxy = delta_matrix(x, y)
    myx = -np.moveaxis(mxy, 0, 1)

    rx = norm(mx, 2)
    ry = norm(my, 2)
    rxy = norm(mxy, 2)
    ryx = rxy.T

    with np.errstate(invalid='ignore'):
        vx = np.nansum(expand(g(rx / 2, 1)) * mx, axis=1) + \
            np.nansum(expand(g(rxy / 2, 3)) * mxy, axis=1)
        vy = np.nansum(expand(g(ry / 2, 2)) * my, axis=1) + \
            np.nansum(expand(g(ryx / 2, 3)) * myx, axis=1)
    vx /= N1
    vy /= N1

    for s in [0, 10, 20, 30, 40, 50, 60, 70, 100, 150, 200, 300, 600, 1000]:
        if abs(t * dt - s) < dt / 2:
            sp.quiver(x, vx, color='blue')
            sp.quiver(y, vy)
            # sp.text('t=%.1f' % (t * dt))
            sp.ax.set_aspect('equal', 'box')
            sp.ax.axis('off')
            sp.fig.savefig(
                f'particle/two/b3={b[2]}.mu={mu}.t={t * dt}.pdf')
            sp.ax.cla()

    # plt.scatter(*(x.T), s=5, color='purple')
    # plt.scatter(*(y.T), s=5, color='black')
    # ax.text(-.1, 1.1, 't=%.1f' % (t * dt))
    # camera.snap()

    x += vx * dt
    y += vy * dt

# animation = camera.animate(interval=0)
# plt.show()
# print('Saving to mp4...', end='\r')
# animation.save(f'particle/two-species{b[2]}.mp4', dpi=200, fps=frakit.FPS)
# print('Done!')
# print('\033[F\033[K')
