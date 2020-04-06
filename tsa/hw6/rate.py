import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

data = pd.read_excel('hw6/NYSEReturns.38135430_第三章.xlsx')
X = data['RATE'].dropna().to_numpy()

plt.plot(X)
sm.graphics.tsa.plot_acf(X)
sm.graphics.tsa.plot_pacf(X)

plt.show()
