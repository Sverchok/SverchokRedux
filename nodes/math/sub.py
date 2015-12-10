import numpy as np
from ..svtyping import Number


def sub(x: Number = 0.0, y: Number = 1.0) -> [("res", Number)]:
    return x - y


def mul(x: Number = 0.0, y: Number = 1.0) -> [("res", Number)]:
    return x * y


SvRxFunc = [sub, mul]
