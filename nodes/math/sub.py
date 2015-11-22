import numpy as np


def sub(x: np.array = 0.0, y: np.array = 1.0) -> [("res", np.array)]:
    return x - y

def mul(x: np.array = 0.0, y: np.array = 1.0) -> [("res", np.array)]:
    return x * y

SvRxFunc = [sub, mul]
