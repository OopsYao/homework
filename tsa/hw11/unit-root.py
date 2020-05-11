from arch.unitroot import ADF, PhillipsPerron
import pandas as pd
import numpy as np

data = pd.read_excel('hw11/quarterly.7775706_第一章.xlsx')
ind_prod = data['IndProd'].dropna().to_numpy()
ln_rgdp = np.log(data['RGDP'].dropna().to_numpy())

# ADF test
for lags in (12 - i for i in range(12)):
    ind_prod_adf = ADF(ind_prod, lags)
    print(ind_prod_adf.summary())
