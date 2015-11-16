# helper functions


def intsocket(name, default_value=1):
    return "SvRxIntSocket", name, default_value


def floatsocket(name, default_value=1):
    return "SvRxFloatSocket", name, default_value


def meshsocket(name):
    return "SvRxMeshSocket", name


def stringsocket(name):
    return "SvRxStringSocket", name


def vectorsocket(name):
    return "SvRxVectorSocket", name
