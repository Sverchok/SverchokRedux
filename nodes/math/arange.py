import numpy as np

def arange(start : int = 0, stop : int = 10, step : int = 1) -> [("range", np.array)]:
    return np.arange(start, stop, step)

arange.label = "Range"

SvRxFunc = [arange]
