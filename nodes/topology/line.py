import numpy as np


def mesh_line(vertices: np.ndarray=0) -> [("edges", np.ndarray)]:
    l = len(vertices)
    out = np.zeros((l - 1, 2), dtype=np.int32)
    out[:, 0] = np.arange(0, l - 1)
    out[:, 1] = np.arange(1, l)
    return out

SvRxFunc = [mesh_line]
