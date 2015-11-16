import numpy as np

def linspace(start : float = 0.0, stop : float = 1.0, count : int = 10) -> [("linspace", np.array)]:
    return np.linspace(start, stop, num)

linspace.label = "Linear space"
