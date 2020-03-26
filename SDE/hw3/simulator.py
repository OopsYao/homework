import numpy as np
import matplotlib.pyplot as plt
import math

T = 10
dt = 0.001
steps = int(T / dt)
np.random.seed(1)

def sample_path_generator(mu, sigma, x0=1):
    # Independent dx
    dx = np.exp(
        mu * dt
        + sigma * np.random.normal(0, np.sqrt(dt), steps)
    )
    dx = np.hstack([np.ones(1), dx])
    # Their product as accumulation
    x = x0 * dx.cumprod(axis=0)
    return x

for mu, sigma in [(1, 0.4), (1, 0.8), (0.5, 0.4), (-0.3, 0.4)]:
    path = sample_path_generator(mu, sigma)
    plt.plot(np.linspace(0, T, 1 + steps), path, label=f'$\mu={mu},\sigma={sigma}$')

plt.legend()
plt.xlabel('t')
plt.ylabel('X')
plt.title(f'$T = {T}$')
plt.show()