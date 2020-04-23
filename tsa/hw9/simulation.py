import numpy as np
import matplotlib.pyplot as plt

sigma = 2
T = 100
y0 = 0

np.random.seed(1)


def simulate(mu, alpha):
    epsilon = sigma * np.random.normal(size=T)
    dy = epsilon + mu + alpha * np.arange(1, T + 1)
    np.insert(dy, 0, 0)  # First offset is 0
    y = y0 + dy.cumsum()

    if mu != 0:
        label = f'With constant $\\mu={mu}$'
        if alpha != 0:
            label += f' and trend $\\alpha={alpha}$'

    plt.plot(y, label=label)


simulate(0.1, 0)
simulate(0.1, 0.01)

plt.legend()
plt.xlabel('$t$')
plt.ylabel('$y$')
plt.show()
