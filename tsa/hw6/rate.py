import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.stattools as stattools
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
from arch.univariate import ARX, GARCH
from arch import arch_model

data = pd.read_excel('hw6/NYSEReturns.38135430_第三章.xlsx')
rates = data['RATE'].dropna().to_numpy()

# Statistic description
plt.plot(rates)
sm.graphics.tsa.plot_acf(rates)

# ARCH effect
ar_res = AutoReg(rates, lags=[1]).fit()
# Test of no serial correlation and homoskedasticity
print(ar_res.diagnostic_summary())

a = ar_res.resid
a_res = ar_select_order(a, 5).model.fit()
print(a_res.diagnostic_summary())

# Fit with GARCH(p, q)
ar = ARX(rates, lags=[1])  # Mean model
ar.volatility = GARCH(p=4, q=1)  # Volatility model

res = ar.fit()
res.plot()
# plt.plot(res.resid)
print(res.summary())
plt.show()
