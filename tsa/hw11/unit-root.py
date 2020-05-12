from arch.unitroot import ADF, PhillipsPerron

from statsmodels.tsa.ar_model import AutoReg, ar_select_order
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_excel('hw11/quarterly.7775706_第一章.xlsx')
ind_prod = data['IndProd'].dropna().to_numpy()
ln_rgdp = np.log(data['RGDP'].dropna().to_numpy())


def unitroot_test(series):
    # Basic statistic
    plt.figure()
    plt.plot(series)
    plot_pacf(series)

    # ADF test
    # AIC & BIC from lags 12 to 1
    print('$p$ & AIC & BIC \\\\')
    max_lags = 12
    for lags in (max_lags - i for i in range(max_lags)):
        ar_model = AutoReg(series, lags, 'n')
        res = ar_model.fit()
        print(f'{lags} & {round(res.aic, 3)} & {round(res.bic, 3)} \\\\')

    # Best lags by `ar_select_order`
    sel = ar_select_order(series, max_lags, trend='n')
    lags = sel.ar_lags[-1]
    print(f'Lags selection: {sel.ar_lags}')

    # Start ADF test
    adf = ADF(series, lags)
    print(adf.summary())

    # PP test
    pp_tau = PhillipsPerron(series, 3, test_type='tau')  # q = 3
    pp_rho = PhillipsPerron(series, 3, test_type='rho')  # q = 3
    print(pp_tau.summary())
    print(pp_rho.summary())


# unitroot_test(ind_prod)
unitroot_test(ln_rgdp)
plt.show()
