import numpy as np
import matplotlib.pyplot as plt
from utils import delta_matrix, norm, expand
from anikit import ShootPlot
from forcelib import Morse, hyper_tang
from misc import snap_iter

D = 2  # Dimension
N = 400  # Number of prey
# N2 = 1

# Randomly initial distribution
np.random.seed(0)
x = 2 * np.random.rand(N, D)
# z = np.random.rand(N2, D)
z = np.array([
    [-0.1, 0.5],
    # [2.1, 0.7],
    # [-0.1, 0.3],
    # [2.1, 0.1],
])
N2 = len(z)

c = 2
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


def system_generator(x0, z0, dt):
    t = 0
    x = x0
    z = z0

    while True:
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

        yield t, x, z, vx, vz

        x = x + vx * dt
        z = z + vz * dt
        t += dt


if __name__ == '__main__':
    dt = 0.02
    c = 10
    sp = ShootPlot()
    for s, x, z, vx, vz in snap_iter(
        np.hstack((
            np.linspace(0, 2, 50),
            np.linspace(2, 10, 20),
            np.linspace(10, 100, 10),
            np.linspace(100, 300, 10),
        )),
        system_generator(x, z, dt),
        dt
    ):
        sp.quiver(x, vx, color='black')
        sp.quiver(z, vz, color='red', minlength=1)
        sp.save(f'particle/prey/N2={N2}.c={c}.t={s:.2f}.pdf')
        sp.clear()
    #     sp.scatter(x)
    #     sp.scatter(z, color='blue')
    #     sp.text(f't={s:.2f}')
    #     sp.snap()
    # ani = sp.animate()
    # ani.save(f'particle/prey/N2={N2}.c={c}.mp4', dpi=200, fps=60)

    # z_trace = []
    # t_trace = []
    # for s, x, z, vx, vz in snap_iter(
    #     np.linspace(0, 40, 2000),
    #     system_generator(x, z, dt),
    #     dt
    # ):
    #     z_trace.append(z)
    #     t_trace.append(s)
    # z_trace = np.array(z_trace)
    # z_trace = np.moveaxis(z_trace, 0, 1)

    # # fig, ax = plt.subplots(1, 2)
    # plt.figure(figsize=(10, 4))
    # plt.subplot(121)
    # color_scheme = ['black',  'red', 'green', 'blue', 'black']
    # i = 0
    # for pred in z_trace:
    #     plt.plot(t_trace, pred[:, 0], color=color_scheme[i],
    #              label=f'predator {i + 1} vx')
    #     plt.plot(t_trace, pred[:, 1], color=color_scheme[i],
    #              linestyle='--', label=f'predator {i + 1} vy')
    #     i += 1
    # plt.legend()
    # plt.xlabel('t')
    # plt.ylabel('v')

    # plt.subplot(122)
    # i = 0
    # for pred in z_trace:
    #     plt.plot(pred[:, 0], pred[:, 1], color=color_scheme[i],
    #              label=f'predator {i + 1}')
    #     i += 1
    # plt.legend()
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.tight_layout(pad=0)
    # plt.savefig(f'func-pre{N2}.c={c}.pdf')
    # plt.show()
