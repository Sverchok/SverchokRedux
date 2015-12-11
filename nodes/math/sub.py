from ..svtyping import Number
from ..decorators import node_func

@node_func(label="Subtract")
def sub(x: Number = 0.0, y: Number = 1.0) -> [("res", Number)]:
    return x - y

@node_func(label="Mult")
def mul(x: Number = 0.0, y: Number = 1.0) -> [("res", Number)]:
    return x * y


SvRxFunc = [sub, mul]
