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
ar_res = ar_select_order(rates, 5).model.fit()
# Test of no serial correlation and homoskedasticity
print(ar_res.diagnostic_summary())
print(ar_res.summary())
plt.figure()
plt.plot(ar_res.resid)

# a = ar_res.resid
# a_res = ar_select_order(a, 5).model.fit()
# print(a_res.diagnostic_summary())

# Fit with GARCH(p, q)
ar = ARX(rates, lags=[1, 2])  # Mean model
ar.volatility = GARCH(p=1, q=1)  # Volatility model
res = ar.fit()
res.plot()
print(res.summary())

# Forecast
drop = len(data) - len(rates)
start = 3254 - 2 - drop
end = 3262 - 2 - drop

var = res.forecast(start=start, horizon=5,
                   method='simulation').variance[start:1+end]
var.plot()
entry = [
    '2012:06:20',
    '2012:06:21',
    '2012:06:22',
    '2012:06:25',
    '2012:06:26',
    '2012:06:27',
    '2012:06:28',
    '2012:06:29',
    '2012:07:02',
]
for v, e in zip(var['h.1'], entry):
    print(f'{e} & {round(v,4)} \\\\')

plt.show()