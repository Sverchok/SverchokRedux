import numpy as np


def sv_zip(a: np.ndarray = 0, b: np.ndarray = 0) -> [("res", np.ndarray)]:
    l = min(len(a), len(b))
    out = np.zeros((l, 2), dtype=a.dtype)
    out[:, 0] = a[:l]
    out[:, 1] = b[:l]
    return out

sv_zip.label = "Zip"

SvRxFunc = [sv_zip]
