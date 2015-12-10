import numpy as np
from ..svtyping import Number
from ..decorators import node_func

@node_func
def add(x: Number = 0.0, y: Number = 1.0) -> [("res", Number)]:
    return x + y
