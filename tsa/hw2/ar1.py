import numpy as np
import math
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.tsa.stattools as stattools

N = 100
Z = np.random.normal(size=N) 
def generate(f):
    # Here X1 means X_{t-1}
    X1 = 0 # Suppose X_0 = 0 if needed but not defined
    X = []
    for t, (Z1, Z0) in enumerate(
        zip(Z, np.append(Z[1:], Z[:1])), 
        start=1):
        X1 = f(X1, Z0, Z1, t)
        X.append(X1)
    return np.array(X)

Xa = generate(lambda X1, Z0, Z1, t: Z0)
Xb = generate(lambda X1, Z0, Z1, t: -0.3 * X1 + Z0)
Xc = generate(lambda X1, Z0, Z1, t: math.sin(math.pi / 3 * t) + Z0)
Xd = generate(lambda X1, Z0, Z1, t: Z0 - 0.3 * Z1)
np.delete(Xd, len(Xd) - 1)
Xe = generate(lambda X1, Z0, Z1, t: 2 - 3 * t + Z0)

def draw(X):
    plt.plot(range(1, 1+len(X)), X)
    plt.xlabel("t")
    sm.graphics.tsa.plot_acf(X, lags=len(X)-1)
    plt.xlabel("Lag")

def p_QLB(X):
    _, Q, p = stattools.acf(X, qstat=True)
    for m in [6, 12]:
        print(f'Give m = {m}: Q = {Q[m - 1]}, p = {p[m - 1]}')

    for m in [6, 12]:
        print(f'{m} & {Q[m - 1]} & {p[m - 1]}\\\\')

def all(X):
    draw(X)
    p_QLB(X)
all(Xe)
plt.show()