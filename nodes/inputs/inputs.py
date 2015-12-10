from ..svtyping import ValueFloat, ValueInteger
from ..decorators import node_func


@node_func(label="Input Int")
def int_in() -> [("Value", ValueInteger)]:
    pass

def float_in() -> [("Value", ValueFloat)]:
    pass

SvRxFunc = [float_in, int_in]
