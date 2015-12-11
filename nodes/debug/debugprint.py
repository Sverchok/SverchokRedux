import pprint
from ..svtyping import Generic
from ..decorators import node_func


@node_func
def debug_print(data: Generic) -> None:
    pprint.pprint(data)
