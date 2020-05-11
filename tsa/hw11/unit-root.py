from arch.unitroot import ADF, PhillipsPerron
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
import pandas as pd
import numpy as np

data = pd.read_excel('hw11/quarterly.7775706_第一章.xlsx')
ind_prod = data['IndProd'].dropna().to_numpy()
ln_rgdp = np.log(data['RGDP'].dropna().to_numpy())


def unitroot_test(series):
    # ADF test
    # AIC & BIC from lags 12 to 1
    print('AIC & BIC \\\\')
    for lags in (12 - i for i in range(12)):
        ar_model = AutoReg(series, lags, 'n')
        res = ar_model.fit()
        print(f'{round(res.aic, 3)} & {round(res.bic, 3)} \\\\')

    # Best lags by `ar_select_order`
    sel = ar_select_order(series, 12, trend='n')
    print(f'Lags selection: {sel.ar_lags}')

    # Start ADF test
    adf = ADF(series, sel.ar_lags[-1])
    print(adf.summary())

    # PP test
    pp = PhillipsPerron(ind_prod)
    print(pp.summary())


unitroot_test(ind_prod)
unitroot_test(ln_rgdp)
