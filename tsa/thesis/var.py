import numpy as np
import pandas as pd

from arch.unitroot import ADF
from statsmodels.tsa.api import VAR

import seaborn as sns
import matplotlib.pyplot as plt

# Seaborn theme for graphing
sns.set()


def split_line(text=None):
    if text == None:
        print('=================================')
    else:
        print(f'''
=========================================
{text}
=========================================
        ''')


data = pd.read_csv('thesis/tourists.csv')
yearly = pd.to_datetime({'year': data['年份'], 'month': 1, 'day': 1})
mdata = pd.DataFrame({
    'num': data['国内游客(百万人次)'],
    'cost': data['国内旅游总花费(亿元)'],
    'GDP': data['GDP(亿元)']
})
mdata.index = pd.DatetimeIndex(yearly)
mdata = mdata.dropna()

num = mdata['num']
cost = mdata['cost']
GDP = mdata['GDP']


def trend_plot(series):
    plt.figure()
    series.plot()


trend_plot(num)
trend_plot(cost)
trend_plot(GDP)


def ADF_test(series):
    print(ADF(series, trend='nc').summary())


ADF_test(mdata['num'])
ADF_test(mdata['cost'])
ADF_test(mdata['GDP'])


# Fit with VAR
results = VAR(mdata).fit(verbose=True, trend='nc')
results.plot()
print(results.summary())
# Selected lag order
print('Auto-selected Order:', results.k_ar)

# Stability
print()
print('Stability test:')
print(results.is_stable(True))

# Residual normality
print()
print(results.test_normality().summary())

# Granger causality
names = ['num', 'cost', 'GDP']
print()
for n in names:
    print('Granger for', n)
    # Factor `n` caused by its complement
    print(results.test_causality(n, list(set(names) - set(n))).summary())

# Impulse Response Analysis
irf = results.irf(10)
irf.plot(orth=False)

# Forecast Error Variance Decomposition
fevd = results.fevd(5)
print()
print(fevd.summary())
fevd.plot()

# plt.show()
