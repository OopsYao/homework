import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

T = 500
dt = 0.1
W0 = 0
np.random.seed(100)

dW = (dt ** 0.5) * np.random.normal(size=int(T / dt))
W = np.insert(np.cumsum(dW), 0, W0)
X = 1 / (1 - W)

hitting_time = np.where(np.abs(W - 1) <= 0.005)[0][0] / int(T / dt) * T
plt.axvline(x=hitting_time, linestyle='--',
            label='hitting time', color='k', linewidth=0.75)
plt.plot(np.linspace(0, T, len(X)), X)
plt.xlabel('t')
plt.legend()


def hitting(maxT):
    size = int(maxT / dt)
    dW = (dt ** 0.5) * np.random.normal(size=size)
    W = np.insert(np.cumsum(dW), 0, W0)
    try:
        time = np.where(np.abs(W - 1) <= 0.005)[0][0] / size * maxT
    except:
        time = maxT
    return time


trials = 1000
for T in [1000, 5000, 10000]:
    series = [hitting(T) for i in range(trials)]
    plt.figure()
    sns.distplot(series)
    est = sum(series) / trials
    print(est)
plt.show()
