import numpy as np
import matplotlib.pyplot as plt


b = .1 
a1 = 1
a2 = 1

x = np.linspace(0, 20, 1000)
y1 = np.tanh(a1 * (1 - x)) + a2
y2 = b / x

plt.plot(x, y1, label=f'hyperbolic tangent, $a_1={a1},a_2={a2}$')
plt.plot(x, y2, label=f'inverse proportional, $b={b}$')
plt.ylim((0, 4))

plt.xlabel('r')
plt.legend()
plt.show()