from progressbar import progressbar
import numpy as np
import math
from numpy import linalg as LA
import matplotlib.pyplot as plt

dt = 0.001
N = 200
U = 1
g = 1

position = 3 * np.random.rand(N, 2)
velocity = np.zeros((N, 2))

trace = []


def q(r):
    G = 0.5
    L = 10
    return G * math.exp(- r / L) - math.exp(-r)


def attrack(r):
    norm = LA.norm(r)
    return q(norm) / norm * r


def r_mat(position):
    mat = [[0 for x in range(N)] for y in range(N)]
    for i in range(N):
        for j in range(N):
            mat[i][j] = position[j] - position[i]
    return mat


for _ in progressbar(range(int(2 / dt))):
    trace.append(position[0])
    position += velocity * dt
    r = r_mat(position)

    v = []
    for i in range(N):
        v.append(sum(
            attrack(r[i][j]) for j in range(N) if i != j
        ))
    v = np.array(v).reshape((N, 2))
    velocity = np.tile([U, -g], (N, 1)) + v
plt.scatter(*(position.T))
plt.show()
