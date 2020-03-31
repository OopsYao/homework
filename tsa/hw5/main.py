import statsmodels.tsa.arima_model as ARIMA_model
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stattools

from termcolor import colored, cprint 
  
def sad(text):
    print(colored(text, 'red', attrs=['reverse', 'blink']))

def tada(text):
    print(colored(text, 'green', attrs=['reverse', 'blink']))

def info(text):
    print(text)

data = pd.read_excel('hw5/quarterly.7775706_第一章.xls')
unemp = data['Unemp'].dropna()

X = np.log(unemp.to_numpy())

# Determine d
def visual_stable(X, d=0):
    if d != 0:
        X = np.diff(X, n=d)
    # plt.plot(X)
    sm.graphics.tsa.plot_acf(X)

visual_stable(X)
visual_stable(X, 1)
visual_stable(X, 2)

d = 1

# Determine p, q
sm.graphics.tsa.plot_acf(np.diff(X, n=d))
sm.graphics.tsa.plot_pacf(np.diff(X, n=d))

# Fit with ARIMA(p, d, q)
model = ARIMA_model.ARIMA(X, (1, d, 4))
result = model.fit()
print(result.summary())

# Residual test
# Note that the prediction loses d of data, so the original data
# should drop first-d elements to match.
residual = np.delete(X, range(d)) - result.predict(typ='levels')
result.plot_predict()

_, Q, p = stattools.acf(residual, qstat=True)
Q6, Q12 = Q[5], Q[12]
p6, p12 = p[5], p[12]
if p6 < 0.05 or p12 < 0.05:
    sad('Bad! Not a white noise, test failed')
    if p6 >= 0.05:
        sad(f'Since p12 = {round(p12, 4)} < 0.05')
    else:
        sad(f'Since p6 = {round(p6, 4)} < 0.05')
else:
    tada('Good! Residual is white noise, test passed')
    Q6 = round(Q6, 4)
    p6 = round(p6, 4)
    Q12 = round(Q12, 4)
    p12 = round(p12, 4)
    info(f'Q6 = {Q6}, p6 = {p6}')
    info(f'Q12 = {Q12}, p12 = {p12}')
    # Generate LaTeX table
    print('LaTeX tabular')
    print(f'6 & {round(Q6, 4)} & {round(p6, 4)}\\\\')
    print(f'12 & {round(Q12, 4)} & {round(p12, 4)}\\\\')

# In-sample prediction
tail_start = len(X) - 8
result.plot_predict(tail_start)
last_prediction = result.predict(tail_start, typ='levels')
print('Real vs Prediction')
for i, (pred, real) in enumerate(zip(last_prediction, X[tail_start::])):
    print(f'{2011 + i // 4}Q{i % 4 + 1} & {round(real, 5)} & {round(pred, 5)} & {round(real - pred, 5)}\\\\')
plt.show()