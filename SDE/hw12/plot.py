import numpy as np
from numpy.random import RandomState, SeedSequence, MT19937
import matplotlib.pyplot as plt

rs = RandomState(MT19937(SeedSequence(1024)))

T = 1
N = 2000
dt = T / N


def path():
    dW = rs.normal(scale=dt ** 0.5, size=(N, 2))
    dW = np.vstack((np.zeros(2), dW))
    Wt = np.cumsum(dW, axis=0)
    return Wt.T


# Uniform event for different parameter paris
pathA, pathB = path()

color_map = ['#eac435', '#345995', '#e40066', '#03cea4']

t = np.linspace(0, T, N + 1)
for (alpha, beta), c in zip([(0.5, 0.5), (0.5, 1), (1, 0.5), (1, 1)], color_map):
    # Different event for different params
    pathA, pathB = path()
    plt.plot(t, np.exp(alpha * t + beta * pathA),
             label=f'$\\alpha={alpha},\\beta={beta}$', color=c)
    plt.plot(t, np.exp(alpha * t + beta * pathB),
             color=c)
    plt.plot(t, np.exp((alpha + beta ** 2 / 2) * t),
             color=c)
plt.ylim(0, 5)
plt.xlabel('t')
plt.title(
    '$f(t,W_t)=\\exp(\\alpha t+\\beta W_t),Ef(t,W_t)=\\exp((\\alpha+\\beta^2/2)t)$')
plt.legend()
plt.show()
