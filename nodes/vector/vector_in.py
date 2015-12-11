import numpy as np
from ..svtyping import Number, Vertices
from ..decorators import node_func

@node_func(label="Vector in")
def vector_in(x: Number = 0.0, y: Number = 0.0, z: Number = 0.0) -> [("vec", Vertices)]:
    out = np.zeros((len(x), 3))
    out[:, 0] = x
    out[:, 1] = y
    out[:, 2] = z
    return out
