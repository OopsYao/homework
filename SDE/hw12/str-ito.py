import numpy as np
from numpy.random import RandomState, SeedSequence, MT19937

rs = RandomState(MT19937(SeedSequence(12345678911)))

T = 1


def case(N):
    dt = T / N
    dW = rs.normal(scale=dt ** 0.5, size=N)
    dW = np.insert(dW, 0, 0)
    Wt = np.cumsum(dW)
    dW = dW[1:]

    Ito = sum(w * dw for w, dw in zip(Wt[:-1], dW))
    Stratonovich = sum((w1 + w2) / 2 * dw for w1,
                       w2, dw in zip(Wt[:-1], Wt[1:], dW))

    return Stratonovich - Ito - 1/2


for k in [2, 4, 6, 8, 10]:
    print(f'$2^{{{k}}}$ & ${round(abs(case(2 ** k)), 5)}$\\\\')
