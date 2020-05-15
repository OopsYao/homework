from scipy.io import loadmat

from statsmodels.tsa.ar_model import AutoReg
import numpy as np
import matplotlib.pyplot as plt

mat = loadmat('hw9/FTSE.mat')
FTSE = np.array(mat['FTSE']).flatten()

np.random.seed(0)

# AR(1) (OLS)
dt = 1
res = AutoReg(FTSE, 1).fit()
s2 = sum(r ** 2 for r in res.resid) / res.df_resid

r = res.params[0] / dt
mu = (1 - res.params[1]) / dt
sigma = (s2 / dt) ** 0.5
print('r:', format(r, '.3g'))
print('mu:', format(mu, '.3g'))
print('sigma:', format(sigma, '.3g'))

# Simulation
# res.plot_predict(dynamic=True)  # Following can be replaced by this line
# sigma = 0
plt.plot(FTSE, label='Real path')
X0 = FTSE[0]
X = [X0]
for i in range(len(FTSE) - 1):
    last = X[-1]
    X.append(last + (r - mu * last) * dt)
plt.plot(X, label='$\\sigma=0$')
# Asymptote
plt.plot(r / mu * np.ones(len(FTSE) - 1),
         label='Asymptote ($r/\\mu$)', linestyle='--')

# sigma != 0
dws = np.random.normal(size=len(FTSE) - 1) * (dt ** 0.5)
Y = [X0]
for dw in dws:
    last = Y[-1]
    Y.append(last + (r - mu * last) * dt + sigma * dw)
plt.plot(Y, label='Simulation ($\\sigma\\neq 0$)')
plt.legend()
plt.show()
