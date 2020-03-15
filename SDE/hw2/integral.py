import scipy.integrate as integrate
import matplotlib.pyplot as plt
import numpy as np
import math

delta_t = 1
L = 1
N = 10
def p_generator(N):
    def inner(*w):
        s = sum(
            (wt - wt1)**2 for wt, wt1 in zip(w, (0, ) + w)
        )
        return math.exp(-s / 2 / delta_t) / (2 * math.pi * delta_t) ** (N / 2)
    return inner

@np.vectorize
def P(N):
    return integrate.nquad(p_generator(N), [(-L , L) for i in range(N)])[0]

X = range(1, 7)
plt.scatter(X, P(X))
plt.show()