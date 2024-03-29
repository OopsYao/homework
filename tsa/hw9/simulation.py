import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

import seaborn as sns

sigma = 2
T = 800
y0 = 0

np.random.seed(1)


def simulate(mu, alpha, unit_root=False):
    if unit_root:
        epsilon = np.random.normal(size=T)
        u = [0]  # The stable process
        phi = 0.5
        for e in epsilon:
            u.append(phi * u[-1] + e)
        epsilon = np.array(u[1:])
    else:
        epsilon = sigma * np.random.normal(size=T)
    dy = epsilon + mu + alpha * np.arange(1, T + 1)
    np.insert(dy, 0, 0)  # First offset is 0
    y = y0 + dy.cumsum()

    return y


def rho_stat(mu, alpha):
    seq = simulate(mu, alpha)
    base = sum(y1 ** 2 for y1 in seq[:-1])
    return sum(y1 * y0 for y1, y0 in zip(seq[:-1], seq[1:])) / base


plt.plot(simulate(0.01, 0), label='Random walk with constant $\\mu=0.1$')
plt.plot(simulate(0.01, 0.001),
         label='Random walk with constant $\\mu=0.1$ and trend $\\alpha=0.01$')
plt.plot(simulate(0.01, 0, True),
         label='Unit root process with constant $\\mu=0.1$')
plt.xlabel('$t$')
plt.ylabel('$y$')
plt.legend()

# rho statistic
N = 10000  # N times experiments
rho = np.array([rho_stat(0.1, 0.01) for i in range(N)])

plt.figure()
sns.distplot(rho, label='HIST')
# Fit with normal dist
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, *(norm.fit(rho)))
plt.plot(x, p, color='#00aaffff', linestyle='-.', label='Normal density fit')
plt.legend()
plt.title(f'$\\hat\\rho$ of {N} experiments')
plt.xlabel('$\\hat\\rho$')

plt.show()
