import numpy as np


def add(x: np.ndarray = 0.0, y: np.ndarray = 1.0) -> [("res", np.ndarray)]:
    return x + y

SvRxFunc = [add]
