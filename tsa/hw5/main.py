import statsmodels.tsa.arima_model as ARIMA_model
import statsmodels.api as sm
import statsmodels.tsa.api as tsa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel('hw5/quarterly.7775706_第一章.xls')
unemp = data['Unemp'].dropna()
tail = unemp.tail(4 * 2)
# unemp.drop(unemp.tail(4 * 2).index, inplace=True)

X = np.log(unemp.to_numpy())

plt.plot(X)
plt.xlabel('Quarter')
plt.ylabel('$\ln\mathrm{Unemp}$')
sm.graphics.tsa.plot_acf(X)
sm.graphics.tsa.plot_pacf(X)

model = ARIMA_model.ARIMA(X, (2, 1, 0))
result = model.fit()
print(result.summary())

result.plot_predict()

plt.show()