import numpy as np
import pandas as pd

from arch.unitroot import ADF
from statsmodels.tsa.api import VAR
import statsmodels.formula.api as smf

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


LIT_NUM = '国内游客(百万人次)'
LIT_COST = '国内旅游人均花费(元)'
LIT_GDP = '人均国内生产总值(元)'

data = pd.read_csv('thesis/tourists.csv')
yearly = pd.to_datetime({'year': data['年份'], 'month': 1, 'day': 1})
mdata = pd.DataFrame({
    'num': data[LIT_NUM],
    'cost': data[LIT_COST],
    'GDP': data[LIT_GDP]
})
mdata.index = pd.DatetimeIndex(yearly)
mdata = mdata.dropna().sort_index()
mdata = np.log(1 + mdata)

num = mdata['num']
cost = mdata['cost']
GDP = mdata['GDP']


def ADF_test(series):
    print(ADF(series).summary())


ADF_test(mdata['num'])
ADF_test(mdata['cost'])
ADF_test(mdata['GDP'])

# ADF test for delta
ADF_test(mdata['num'].diff().dropna())
ADF_test(mdata['cost'].diff().dropna())
ADF_test(mdata['GDP'].diff().dropna())

# Cointegration
co_res = smf.ols(formula='GDP ~ cost + num - 1', data=mdata).fit()
print(co_res.summary())
ADF_test(co_res.resid)

# Fit with VAR
VAR_model = VAR(mdata)
results = VAR_model.fit(verbose=True)
results.plot()
print(results.summary())
# Selected lag order
print('Auto-selected Order:', results.k_ar)
print(VAR_model.select_order().summary())

# Residual normality
print()
print(results.test_normality().summary())

# Granger causality
names = ['num', 'cost', 'GDP']
print()

for n1 in names:
    for n2 in names:
        if n1 != n2:
            print(results.test_causality(n1, n2).summary())
symbols = ['\\NUM', '\\COST', '\\GDP']
for n1 in symbols:
    for n2 in symbols:
        if n1 != n2:
            print(f'${n2}$不能Granger引起${n1}$')

# Stability
print()
print('Stability test:')
if results.is_stable(True):
    print('Stable :)')
else:
    print('Non-stable')

# Impulse Response Analysis
irf = results.irf(20)
irf.plot()

# Forecast Error Variance Decomposition
fevd = results.fevd(20)
print()
print(fevd.summary())
fevd.plot()

plt.show()
