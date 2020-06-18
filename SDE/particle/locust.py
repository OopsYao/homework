import numpy as np
from multiprocessing import Pool
from numpy import linalg as LA
from progressbar import progressbar
import matplotlib.pyplot as plt
from celluloid import Camera


class Particle:
    def __init__(self, position=np.array([0, 0]), velocity=np.array([0, 0])):
        self.position = position
        self.velocity = velocity


def attraction(ano, the):
    """ Evaluate attraction on `the` by `ano` """
    def q(r):
        G = 0.5
        L = 10
        return G * np.exp(- r / L) - np.exp(-r)
    r = ano.position - the.position
    norm = LA.norm(r)
    if norm == 0:
        return 0
    return q(norm) / norm * r


class System:
    def __init__(self, particle):
        self.particle = particle

    def particle_move(self, the):
        dt = 0.001
        impact = sum(attraction(ano, the) for ano in self.particle)
        U = 1
        g = 1
        the.velocity = impact + np.array([U, -g])
        the.position += the.velocity * dt
        if the.position[1] < 0:
            the.position[1] = 0
        return the

    def evolve(self):
        with Pool(5) as p:
            self.particle = p.map(self.particle_move, self.particle)

    def visual(self):
        pos = np.array([p.position for p in self.particle])
        plt.scatter(*(pos.T), color='black', linewidths=0.5)


N = 200
system = [Particle(position=3 * np.random.rand(2)) for _ in range(N)]
env = System(system)
fig, ax = plt.subplots()
ax.autoscale_view()
camera = Camera(fig)
for _ in progressbar(range(2000)):
    env.evolve()
    env.visual()
    camera.snap()
animation = camera.animate()
animation.save('animation.mp4')
