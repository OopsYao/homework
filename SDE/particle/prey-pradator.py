import numpy as np
import matplotlib.pyplot as plt
from progressbar import progressbar
from celluloid import Camera
from utils import delta_matrix, norm, expand
from anikit import FrameKit, ShootPlot

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
c = 1.5
T = 41
frakit = FrameKit(T)
dt = frakit.dt

fig, ax = plt.subplots()
ax.axis('off')
fig.tight_layout()
camera = Camera(fig)
sp = ShootPlot()
for f in progressbar(range(frakit.frames)):
    t = f * dt

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

    for s in range(T):
        if abs(t - s) < dt / 2:
            sp.quiver(x, vx)
            sp.quiver(z, vz, color='blue')
            sp.ax.axis('off')
            sp.ax.set_aspect('equal', 'box')
            sp.text('t=%.2f' % t)
            sp.fig.savefig(f'particle/prey/c={c}.t={t}.pdf')
            sp.ax.cla()
        
    # camera.snap()
    x += vx * dt
    z += vz * dt

# animation = camera.animate()
# plt.show()
# animation.save(f'particle/prey/prey-pradator{c}.mp4', fps=frakit.FPS, dpi=200)
