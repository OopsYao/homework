import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import math

D = 1


def phi(x):
    return 1 if abs(x) < 1 else 0


def E(f, mu=0, sigma=1):
    trials = 1000
    samples = np.random.normal(mu, sigma, trials)
    return np.sum(np.vectorize(f)(samples)) / trials


@np.vectorize
def u(t, x):
    co = (2 * D) ** 0.5
    return E(lambda z: phi(x + co * z), sigma=t ** 0.5)


@np.vectorize
def ana_u(t, x):
    def integrand(y):
        return np.exp(- (x - y) ** 2 / (4 * D * t)) * phi(y)
    return quad(integrand, -np.inf, np.inf)[0] / (4 * math.pi * D * t) ** 0.5


x = np.linspace(-5, 5, 5000)
plt.plot(x, np.vectorize(phi)(x), label=f't=0')
for t in [0.01, 0.1, 0.5, 1]:
    plt.plot(x, u(0.1, x), label=f't={t}')
plt.title('Probabilistic Representation')
plt.legend()

plt.figure()
plt.title('Analytical Expression')
plt.plot(x, np.vectorize(phi)(x), label=f't=0')
for t in [0.01, 0.1, 0.5, 1]:
    plt.plot(x, ana_u(0.1, x), label=f't={t}')
plt.legend()

plt.show()
