import numpy as np
import matplotlib.pyplot as plt
import math

T = 100
steps = 1000
# leaps = (T / steps) ** 0.5 * np.random.randn(steps)

def sample_path_generator(mu, sigma):
    leaps = (T / steps) ** 0.5 * np.random.randn(steps)
    X = [1]
    last = X[0]
    t = 0
    for mov in leaps:
        t += T / steps
        last *= math.exp(mu * t + sigma * mov)
        X.append(last)
    return X

for mu, sigma in [(0.00001, 0.1), (-0.00001, 0.1), (-0.00001, 0.2)]:
    plt.plot(np.linspace(0, T, 1 + steps), sample_path_generator(mu,sigma), label=f'$\mu={mu},\sigma={sigma}$')
plt.legend()
plt.xlabel('t')
plt.ylabel('X')
plt.show()