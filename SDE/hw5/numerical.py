import numpy as np
import matplotlib.pyplot as plt

# Parameters
T = 1
mu = 0.1
sigma = 2
X0 = 1
dt = 0.0001

steps = int(T / dt)
np.random.seed(1)

dx = 1 + mu * dt + sigma * np.random.normal(0, np.sqrt(dt), steps)
dx = np.insert(dx, 0, 1)  # Insert value 1 as the fisrt element
X = X0 * dx.cumprod()  # Multiply them together

plt.plot(np.linspace(0, T, 1 + steps), X, color='black')

plt.legend()
plt.xlabel('t')
plt.ylabel('X')
plt.show()
