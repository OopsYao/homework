import numpy as np
import matplotlib.pyplot as plt


b = .1 
a1 = 1
a2 = 1

x = np.linspace(0, 20, 1000)
f1 = 1 / x - x
g1 = 1 / 2 * (np.tanh(1 - x) + 1.5)
f2 = np.tanh(1 - x) - .7
g2 = - (np.tanh(1 - x) + 1)
# y2 = b / x
# y3 = 1 / r - r

# plt.plot(x, y1, label=f'hyperbolic tangent, $a_1={a1},a_2={a2}$')
# plt.plot(x, y2, label=f'inverse proportional, $b={b}$')
plt.plot(x, f1, label='$F_1$')
plt.plot(x, g1, label='$G_1$')
plt.plot(x, f2, label='$F_2$')
plt.plot(x, g2, label='$G_2$')

plt.ylim((-5, 20))

plt.xlabel('r')
plt.legend()
plt.show()