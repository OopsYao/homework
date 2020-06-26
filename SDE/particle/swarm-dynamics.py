from utils import delta_matrix, norm
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from progressbar import progressbar
import anikit

N = 800
T = 20
dt = T / anikit.FRAMES


def F(r, n=2):
    return 1 / r ** (n - 1) - r


x = 2 * np.random.rand(N, 2) - np.tile(1, (N, 2))
dB = np.random.randn(int(T / dt), N, 2) * (dt ** .5)
# Stochastic process initial value
Xt = np.tile(.1, (N, 2))

fig, ax = plt.subplots()
ax.axis('off')
fig.tight_layout()
camera = Camera(fig)
for t in progressbar(range(anikit.FRAMES)):
    r = delta_matrix(x)
    r_norm = np.expand_dims(norm(r), axis=-1)

    with np.errstate(divide='ignore', invalid='ignore'):
        v = np.nansum(F(r_norm) / r_norm * r, axis=1) / N + Xt / 10

    # ax.quiver(*(x.T), *(v.T), color='black', width=.003)
    ax.scatter(*(x.T), color='black')
    camera.snap()

    # Bessel process
    # Xt += dB[t] + dt / (2 * Xt)
    # Brownian motion
    Xt += dB[t]

    x += v * dt
animation = camera.animate()
# plt.show()
animation.save('particle/swarm-BM10.mp4', fps=anikit.FPS, dpi=200)
