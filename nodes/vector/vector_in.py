import numpy as np


def vector_in(x: np.ndarray = 0.0, y: np.ndarray = 0.0, z: np.ndarray = 0.0) -> [("vec", np.ndarray)]:
    out = np.zeros((len(x), 3))
    out[:, 0] = x
    out[:, 1] = y
    out[:, 2] = z
    return out

SvRxFunc = [vector_in]
