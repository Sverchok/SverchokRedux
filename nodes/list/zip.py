import numpy as np
from ..svtyping import Number


def sv_zip(a: Number = 0, b: Number = 0) -> [("res", Number)]:
    l = min(len(a), len(b))
    out = np.zeros((l, 2), dtype=a.dtype)
    out[:, 0] = a[:l]
    out[:, 1] = b[:l]
    return out

sv_zip.label = "Zip"

SvRxFunc = [sv_zip]
