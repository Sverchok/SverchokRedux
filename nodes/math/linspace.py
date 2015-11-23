import numpy as np

def linspace(start : float = 0.0, stop : float = 1.0, count : int = 10) -> [("linspace", np.ndarray)]:
    return np.linspace(start, stop, count)

linspace.label = "Linear space"

SvRxFunc = [linspace]
