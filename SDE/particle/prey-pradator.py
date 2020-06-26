import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from progressbar import progressbar
from celluloid import Camera
from utils import delta_matrix, norm, expand
import anikit

D = 2  # Dimension
N = 400  # Number of prey

# Randomly initial distribution
x = np.random.rand(N, D)
z = np.random.rand(D)

a = 1
b = 0.2
p = 3
c = 2.5
T = 20
dt = T / anikit.FRAMES

fig, ax = plt.subplots()
ax.axis('off')
fig.tight_layout()
camera = Camera(fig)
for t in progressbar(range(anikit.FRAMES)):

    m = delta_matrix(x)
    m_norm = expand(norm(m, 2))
    with np.errstate(divide='ignore', invalid='ignore'):
        social = (1 / m_norm - a) * m
        social = np.nan_to_num(social)

    # axis 1 is the dummy varible
    social = social.sum(axis=1) / N

    zx = x - np.tile(z, (N, 1))
    vx = social + b * zx / expand(norm(zx, 2))
    vz = c / N * (zx / expand(norm(zx, p))).sum(axis=0)

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
animation.save(f'particle/prey-pradator{c}.mp4', fps=anikit.FPS, dpi=200)
