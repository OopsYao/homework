import matplotlib.pyplot as plt
import numpy as np
from utils import delta_matrix, norm, expand
from progressbar import progressbar
from celluloid import Camera
import numpy.testing as npt

# Draw the border
# lx, ux
# ly, uy
border = np.array([
    [0, 1],
    [0, 1]
])
dl = [0.45, 0]
dr = [0.55, 0]
corner = np.array([
    dl,
    border[:, 0],
    border.diagonal(),
    border[:, 1],
    np.fliplr(border).diagonal(),
    dr
])

N = 400
a = 1
b = 0.2
p = 3
c = 0.15
dt = 0.01
T = 2

multiplier = border @ [-1, 1]
shift = border[:, 0]
x = np.random.rand(N, 2) * multiplier + shift
z = np.random.rand(2) * multiplier + shift


def boundary_condition(bias):
    eps = .01
    return (bias <= expand(np.min(bias, axis=-1))) & (bias < eps)


fig, ax = plt.subplots()
ax.autoscale_view()
camera = Camera(fig)
for t in progressbar(range(int(T / dt))):
    plt.plot(*(corner.T), color='r')
    plt.scatter(*(x.T), color='black', s=5)
    plt.scatter(*z, color='blue', s=5)
    camera.snap()

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

    # Boundary condition
    eps = 0.01
    # If at door: |x[0]| <= 1 and |x[1]| < eps
    door = np.expand_dims(
        (np.abs(x - [0.5, 0]) < [0.05, eps]).prod(axis=1), -1)

    bias_l = np.abs(x - border[:, 0])
    bias_u = np.abs(x - border[:, 1])
    low = boundary_condition(bias_l)  # at lower bound
    upp = boundary_condition(bias_u)  # at upper bound
    within = (x < border[:, 1] - [0, eps]) & (x > border[:, 0] + [0, eps])
    bdd = (~ door) & (low | upp) & np.flip(within, -1)

    # Make sure no both reflect
    npt.assert_equal(np.tile(False, N), bdd.prod(axis=-1))

    vx = np.where(bdd, -vx, vx)

    x += vx * dt
    z += vz * dt

camera.animate().save('particle/boxing.mp4', fps=int(T / dt / 10))
