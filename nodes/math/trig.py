import numpy as np


def sin(x: np.ndarray = 0) -> [("res", np.ndarray)]:
    return np.sin(x)


def cos(x: np.ndarray = 0) -> [("res", np.ndarray)]:
    return np.cos(x)


def sin_cos(x: np.ndarray = 0) -> [("sin", np.ndarray), ("cos", np.ndarray)]:
    return np.sin(x), np.cos(x)

SvRxFunc = [sin, cos, sin_cos]
