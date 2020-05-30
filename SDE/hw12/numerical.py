import numpy as np
from numpy.random import RandomState, SeedSequence, MT19937
import matplotlib.pyplot as plt

T = 10
b = 10
r0 = 10.1
N = 2000

rs = RandomState(MT19937(SeedSequence(123456789)))


def case(mu, sigma):

    def alpha(x):
        return mu * (b - x)

    def betaV(x):
        return sigma

    def betaC(x):
        return sigma * (x ** 0.5)

    def solve(alpha, beta, r):
        dt = T / N
        dW = rs.normal(scale=dt ** 0.5, size=N)
        for dw in dW:
            last = r[-1]
            r.append(last + alpha(last) * dt + beta(last) * dw)

    rV = [r0]
    rC = [r0]
    solve(alpha, betaV, rV)
    solve(alpha, betaC, rC)
    return rV, rC


color_map = [
    '#C742D6',
    '#3D5EBA',
    "#f7a278",
    '#17C487',
]
# color_map = ["#6dd3ce", "#c8e9a0", , "#a13d63"]
t = np.linspace(0, T, 1 + N)
for (mu, sigma), c in zip([(1, 1), (0.1, 1), (0.01, 1), (0.01, 0.01)], color_map):
    rV, rC = case(mu, sigma)
    plt.plot(t, rV, label=f'$r_t^V,\\mu={mu},\\sigma={sigma}$', color=c)
    plt.plot(t, rC, label=f'$r_t^C,({mu},{sigma})$',  linestyle='-.', color=c)
plt.xlabel('t')
plt.legend()
plt.show()
