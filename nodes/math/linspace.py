import numpy as np
from bpy.props import BoolProperty


def linspace(start: float = 0.0, stop: float = 1.0, count: int = 10,
             endpoint: BoolProperty() = True) -> [("linspace", np.ndarray)]:
    return np.linspace(start, stop, count, endpoint=endpoint)

linspace.label = "Linear space"

SvRxFunc = [linspace]
