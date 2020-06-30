import numpy as np


def Morse(r, Cr, Ca, lr, la):
    return Cr / lr * np.exp(- r / lr) - Ca / la * np.exp(- r / la)


def hyper_tang(r, a, b):
    return np.tanh(a * (1 - r)) + b


def power_law(r, p, q):
    return r ** (2 * p + 1) / 2 ** p - r ** (2 * q + 1) / 2 ** q


def simple(r, a):
    return 1 / r - a * r
