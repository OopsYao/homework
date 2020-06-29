import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from progressbar import progressbar
from celluloid import Camera
from utils import delta_matrix, norm, expand
from anikit import FrameKit

D = 2  # Dimension
N = 400  # Number of prey
N2 = 3

# Randomly initial distribution
x = 2 * np.random.rand(N, D)
# z = np.random.rand(N2, D)
z = np.array([
    [-0.1, 0.5],
    [2.1, 0.7],
    [-0.1, 0.3],
])

a = 1
b = 0.2
p = 3
q = 2
c = 2.5
T = 20
frakit = FrameKit(T)
dt = frakit.dt

fig, ax = plt.subplots()
ax.axis('off')
fig.tight_layout()
camera = Camera(fig)
for t in progressbar(range(frakit.frames)):

    m = delta_matrix(x)
    m_norm = expand(norm(m, 2))
    with np.errstate(divide='ignore', invalid='ignore'):
        social = (1 / m_norm - a) * m
        social = np.nan_to_num(social)

    # axis 1 is the dummy varible
    social = social.sum(axis=1) / N

    zx = delta_matrix(x, z)
    zx_norm = expand(norm(zx))

    vx = social + b * (zx / (zx_norm ** q)).sum(axis=1)
    vz = c / N * (zx / (zx_norm ** p)).sum(axis=0)

    # ax.quiver(*(x.T), *(vx.T))
    # ax.quiver(*(z.T), *(vz.T), color='blue', width=.003)
    ax.scatter(*(x.T), color='black')
    ax.scatter(*(z.T), color='blue')
    plt.text(-.5, 1.5, 't=%.2f' % (t * dt))
    camera.snap()

    x += vx * dt
    z += vz * dt

animation = camera.animate()
# plt.show()
animation.save(f'particle/prey/prey-pradator{c}.mp4', fps=frakit.FPS, dpi=200)
