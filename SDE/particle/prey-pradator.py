import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from progressbar import progressbar
from celluloid import Camera
from utils import delta_matrix, norm, expand

D = 2  # Dimension
N = 400  # Number of prey


# Randomly initial distribution
x = np.random.rand(N, D)
z = np.random.rand(D)


# def delta_matrix(x):
#     """ Get delta along axis 0, xij = xj - xi """
#     x = np.expand_dims(x, axis=0)
#     return x - np.moveaxis(x, 0, 1)


# def norm(matrix, p=2):
#     # Norm along the last axis
#     norm_matrix = LA.norm(matrix, axis=-1) ** p
#     return np.expand_dims(norm_matrix, axis=-1)


a = 1
b = 0.2
p = 3
c = 0.15
dt = 0.01
T = 1

fig, ax = plt.subplots()
ax.autoscale_view()
camera = Camera(fig)
for t in progressbar(range(int(T / dt))):
    plt.scatter(*(x.T), color='black', s=5)
    plt.scatter(*z, color='blue', s=5)
    # plt.text(0, 0, 't=%.2f' % (t * dt))
    camera.snap()

    m = delta_matrix(x)
    m_norm = expand(norm(m, 2))
    with np.errstate(divide='ignore', invalid='ignore'):
        social = (1 / m_norm - a) * m
        social = np.nan_to_num(social)

    # axis 1 is the dummy varible
    social = social.sum(axis=1) / N

    zx = x - np.tile(z, (N, 1))
    x += (social + b * zx / expand(norm(zx, 2))) * dt

    z += (c / N * (zx / expand(norm(zx, p))).sum(axis=0)) * dt

animation = camera.animate()
# About 6s
animation.save('particle/prey-pradator.mp4', fps=int(T / dt / 6))
