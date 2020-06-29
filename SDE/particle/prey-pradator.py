import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from progressbar import progressbar
from celluloid import Camera
from utils import delta_matrix, norm, expand
import anikit
from funcani import Ani

D = 2  # Dimension
N = 400  # Number of prey
N2 = 5  # Number of predator


a = 1
b = 0.2
p = 3
q = 2
c = .8
T = 20
dt = T / anikit.FRAMES

# fig, ax = plt.subplots()
# ax.axis('off')
# fig.tight_layout()
# camera = Camera(fig)

# Randomly initial distribution
x = np.random.rand(N, D)
z = np.random.rand(N2, D)
vx = np.zeros((N, D))
vz = np.zeros((N2, D))


def hellp(t):
    global x, z, vx, vz
    x += vx * dt
    z += vz * dt

    m = delta_matrix(x)
    m_norm = expand(norm(m, 2))
    with np.errstate(divide='ignore', invalid='ignore'):
        social = (1 / m_norm - a) * m
        social = np.nan_to_num(social)

    # axis 1 is the dummy varible
    social = social.sum(axis=1) / N

    xz = delta_matrix(x, z)
    xz_norm = expand(norm(xz))
    xz_norm_q = xz_norm ** q
    xz_norm_p = xz_norm ** p

    vx = social + b * (xz / xz_norm_q).sum(axis=1)
    vz = c / N * (xz / xz_norm_p).sum(axis=0)

    cx = np.tile((1, 0, 0, 1), (N, 1))
    cz = np.tile((0, 0, 1, 1), (N2, 1))
    return np.vstack((x, z)), np.vstack((vx, vz)) / 1000, np.vstack((cx, cz))


Ani(hellp).start()
# ax.quiver(*(x.T), *(vx.T))
# ax.quiver(*(z.T), *(vz.T), color='blue', width=.003)
# ax.scatter(*(x.T), color='black')
# ax.scatter(*(z.T), color='blue')


# animation = camera.animate()
plt.show()
# animation.save(f'particle/prey-pradator{c}.mp4', fps=anikit.FPS, dpi=200)
