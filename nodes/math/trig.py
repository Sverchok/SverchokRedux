import numpy as np
from ..svtyping import Number
from ..decorators import node_func


@node_func
def sin(x: Number = 0) -> [("res", Number)]:
    return np.sin(x)


@node_func
def cos(x: Number = 0) -> [("res", Number)]:
    return np.cos(x)


@node_func
def sin_cos(x: Number = 0) -> [("sin", Number), ("cos", Number)]:
    return np.sin(x), np.cos(x)
