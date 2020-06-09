import pandas as pd
from statsmodels.tsa.base.datetools import dates_from_str
import numpy as np

from arch.unitroot import ADF
from statsmodels.tsa.api import VAR

import seaborn as sns
import matplotlib.pyplot as plt

sns.set()
data = pd.read_excel('hw12/quarterly.7775706_第一章.xlsx').dropna()
quarterly = dates_from_str(data['DATE'])
mdata = data[['r10', 'Tbill', 'IndProd', 'Unemp']]
mdata.index = pd.DatetimeIndex(quarterly)

mdata['r'] = mdata['r10'] - mdata['Tbill']
mdata['IndProd'] = np.log(mdata['IndProd']).diff()
mdata['Unemp'] = mdata['Unemp'].diff()
mdata = mdata.drop(['r10', 'Tbill'], axis=1).dropna()

# ADF Test
print(ADF(mdata['r']).summary())
print(ADF(mdata['IndProd']).summary())
print(ADF(mdata['Unemp']).summary())

# VAR fit (no constant term)
results = VAR(mdata).fit(ic='bic', verbose=True, trend='nc')
results.plot()
print(results.summary())
# Selected lag order
print('Selected Order:', results.k_ar)

# AIC & BIC of different lags
for p in range(8):
    res = VAR(mdata).fit(p, trend='nc')
    print(res.k_ar, '&', round(res.aic, 6), '&', round(res.bic, 6), '\\\\')

# Stability
print(results.is_stable(True))

# Residual normality
print(results.test_normality().summary())

# Granger causality
names = ['r', 'IndProd', 'Unemp']
for n in names:
    print('Granger for', n)
    # Factor `n` caused by its complement
    print(results.test_causality(n, list(set(names) - set(n))).summary())

# Impulse Response Analysis
irf = results.irf(10)
irf.plot(orth=False)

plt.show()
