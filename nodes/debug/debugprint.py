import pprint
from ..svtyping import Generic


def debug_print(data: Generic) -> None:
    pprint.pprint(data)

SvRxFunc = [debug_print]
