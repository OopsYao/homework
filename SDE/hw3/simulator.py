import numpy as np
import matplotlib.pyplot as plt
import math

T = 50
steps = 500
dt = T / steps
np.random.seed(1)
# leaps = (T / steps) ** 0.5 * np.random.randn(steps)

def sample_path_generator(mu, sigma):
    leaps = dt ** 0.5 * np.random.randn(steps)
    X = [1]
    last = X[0]
    for mov in leaps:
        last *= math.exp(mu * dt + sigma * mov)
        X.append(last)
    return X

for mu, sigma in [(0.00001, 1), (-0.00001, 1), (-0.00001, 1.5)]:
    plt.plot(np.linspace(0, T, 1 + steps), sample_path_generator(mu,sigma), label=f'$\mu={mu},\sigma={sigma}$')

plt.legend()
plt.xlabel('t')
plt.ylabel('X')
plt.show()