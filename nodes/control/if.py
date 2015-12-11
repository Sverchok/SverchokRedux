from ..svtyping import Integer, Generic
from ..decorators import node_func


@node_func(label="If")
def if_node(value: Integer = 1, if_true: Generic = 0, if_false: Generic = 1) -> [("value", Generic)]:
    pass
