import numpy as np
from progressbar import progressbar
from utils import delta_matrix, norm, blind, expand
import matplotlib.pyplot as plt
from celluloid import Camera

D = 2  # Dimension
N = 200
U = 1
G = 0.5
g = 1
T = 10
blind_consideration = False

# Uniform dist in [0, 3] x [0, 3]
x = 3 * np.random.rand(N, D)
v = np.random.rand(N, D) - .5

trace = [x[0]]


def q(r):
    L = 10
    return G * np.exp(- r / L) - np.exp(- r)


dt = 0.01
fig, ax = plt.subplots()
ax.set_aspect('equal')

camera = Camera(fig)
for _ in progressbar(range(int(T / dt))):
    plt.scatter(*(x.T), color='black', s=5)
    camera.snap()

    r = delta_matrix(x)
    r_norm = np.expand_dims(norm(r), axis=-1)
    with np.errstate(divide='ignore', invalid='ignore'):
        social = - np.nan_to_num(q(r_norm) / r_norm * r)

        if blind_consideration:
            valid = expand(blind(v, - r) >= np.cos(np.pi / 4))
            v = np.nansum(social * valid, axis=1) + np.tile([U, -g], (N, 1))
        else:
            v = social.sum(axis=1) + np.tile([U, -g], (N, 1))

    x += v * dt
    # Offland
    x = np.clip(x, [-np.inf, 0], np.inf)
    trace.append(x[0])

_, z_trace = np.array(trace).T
t = np.linspace(0, T, len(z_trace))

plt.figure()
plt.plot(t, z_trace)

animation = camera.animate()
animation.save('particle/locust.mp4', fps=int(T / dt / 10))
# plt.show()
