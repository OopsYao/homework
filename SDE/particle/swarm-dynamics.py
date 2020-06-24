from utils import delta_matrix, norm
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from progressbar import progressbar

N = 800
dt = 0.01
T = 2


def F(r, n=2):
    return 1 / r ** (n - 1) - r


x = 2 * np.random.rand(N, 2) - np.tile(1, (N, 2))
dB = np.random.randn(int(T / dt), N, 2) * (dt ** .5)
# Stochastic process initial value
Xt = np.tile(.1, (N, 2))

fig, ax = plt.subplots()
ax.set_aspect('equal')
camera = Camera(fig)
for t in progressbar(range(int(T / dt))):
    plt.scatter(*(x.T), s=5, color='b')
    camera.snap()

    r = delta_matrix(x)
    r_norm = np.expand_dims(norm(r), axis=-1)

    with np.errstate(divide='ignore', invalid='ignore'):
        v = np.nansum(F(r_norm) / r_norm * r, axis=1) / N + Xt
    x += v * dt
    # Bessel process
    Xt += dB[t] + dt / (2 * Xt)
    # Brownian motion
    # Xt += dB[t]
animation = camera.animate()
plt.show()
# animation.save('particle/swarm-BM.mp4', fps=int(T / dt / 10))
