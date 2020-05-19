import pandas as pd
from arch.unitroot import ADF
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel('hw12/quarterly.7775706_第一章.xlsx')

TBill = data['Tbill'].dropna().to_numpy()
r5 = data['r5'].dropna().to_numpy()
r10 = data['r10'].dropna().to_numpy()
# ADF test for the 3 series
print(ADF(TBill).summary())
print(ADF(r5).summary())
print(ADF(r10).summary())

plt.plot(TBill, label='Tbill')
plt.plot(r5, label='r5')
plt.plot(r10, label='r10')
plt.legend()

# Direct OLS regression
res = smf.ols(formula='Tbill ~ r5 + r10',
              data=data.loc[:, ['Tbill', 'r5', 'r10']].dropna()).fit()
print(res.summary())

# ADF test of residual
# Cointegration test
resid = res.resid
plt.figure()
plt.plot(resid)
plt.title('Residual')
print(ADF(resid))

# ECM
df_ECM = pd.DataFrame({
    'dTBill': np.diff(TBill),
    'dr5': np.diff(r5),
    'dr10': np.diff(r10),
    'u': resid[:-1]
})
ECM = smf.ols(formula='dTBill ~ dr5 + dr10 + u - 1', data=df_ECM).fit()
print(ECM.summary())
plt.show()
