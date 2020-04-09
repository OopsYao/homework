import numpy as np
import matplotlib.pyplot as plt


np.random.seed(1)

def path(n):
    S0 = 0
    dS = np.random.normal(size=n) / (n ** 0.5)
    dS = np.insert(dS, 0, 0)  # First increment is 0
    S = S0 + dS.cumsum()
    plt.plot(np.linspace(0, 1, 1 + n), S, label=f'$n={n}$')


for n in [100, 500, 1000]:
    path(n)
plt.legend()
plt.xlabel('t')
plt.ylabel('S')
plt.show()
