import numpy as np
from ..svtyping import Number


def sin(x: Number = 0) -> [("res", Number)]:
    return np.sin(x)


def cos(x: Number = 0) -> [("res", Number)]:
    return np.cos(x)


def sin_cos(x: Number = 0) -> [("sin", Number), ("cos", Number)]:
    return np.sin(x), np.cos(x)

SvRxFunc = [sin, cos, sin_cos]
