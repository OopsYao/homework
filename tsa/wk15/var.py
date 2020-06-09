import pandas as pd
from statsmodels.tsa.base.datetools import dates_from_str
import numpy as np
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

results = VAR(mdata).fit(ic='bic', verbose=True)
results.plot()
results.plot_acorr()
print(results.summary())
# Selected lag order
print(results.k_ar)

# AIC & BIC of different lags
for p in range(8):
    res = VAR(mdata).fit(p)
    print(res.k_ar, '&', res.aic, '&', res.bic, '\\\\')

plt.show()
