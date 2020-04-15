import numpy as np
import matplotlib.pyplot as plt

# Parameters
T = 200
Y0 = 0

np.random.seed(1)


def simulate(sigma):
    dY = np.random.normal(size=T) * sigma
    dY = np.insert(dY, 0, 0)  # Fisrt offset is 0
    Y = Y0 + dY.cumsum()
    plt.plot(Y, label=f'$\sigma^2={sigma ** 2}$')


for sigma in [1, 2]:
    simulate(sigma)

plt.legend()
plt.xlabel('t')
plt.ylabel('Y')
plt.show()
