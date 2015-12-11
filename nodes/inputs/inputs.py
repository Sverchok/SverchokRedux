from ..svtyping import ValueFloat, ValueInteger
from ..decorators import node_func


@node_func(label="Int Input")
def int_in() -> [("Value", ValueInteger)]:
    pass

@node_func(label="Float Input")
def float_in() -> [("Value", ValueFloat)]:
    pass
