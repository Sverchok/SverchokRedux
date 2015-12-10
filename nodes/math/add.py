import numpy as np
from ..svtyping import Number


def add(x: Number = 0.0, y: Number = 1.0) -> [("res", Number)]:
    return x + y

SvRxFunc = [add]
