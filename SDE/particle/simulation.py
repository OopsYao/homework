from progress.bar import Bar
from atooms.system import System, Particle
from atooms.simulation import Simulation
import math
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt


bar = Bar('Processing')
dt = 0.001
def visual(system):
    plt.figure()
    plt.xlabel('x')
    plt.ylabel('z')
    for p in system.particle:
        plt.scatter(p.position[0], p.position[1])


# Build model system with integer coordinates
N = 200
particle = [Particle() for i in range(N)]
for p in particle:
    p.position = np.array(3 * np.random.rand(3)).flatten()
system = System(particle=particle)
# Initial state
visual(system)


class BareBonesBackend(object):
    def __init__(self, system):
        self.system = system

    def run(self, steps):
        for _ in range(steps):
            self.frame()
            bar.next()

    def q(self, r):
        G = 0.5
        L = 10
        return G * math.exp(- r / L) - math.exp(-r)

    def attraction(self, p):
        delta = [(ano.position - p.position)
                 for ano in self.system.particle if p != ano]

        def norm(vec):
            return LA.norm(vec)
        return sum(self.q(norm(d)) * d / norm(d) for d in delta)

    def frame(self):
        U = 1
        g = 1
        for p in self.system.particle:
            p.position += p.velocity * dt
            p.velocity = self.attraction(p) - np.array([U, -g, 0])


backend = BareBonesBackend(system)
simulation = Simulation(backend)
simulation.run(int(2 / dt))
# simulation.run_until(30)


bar.finish()
visual(system)

plt.show()
