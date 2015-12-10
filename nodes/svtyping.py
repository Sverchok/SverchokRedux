
# big todo, add generics.


class Topology:
    pass


class Vertices:
    pass


class Vector(Vertices):
    pass


class Mesh:
    pass


class String:
    pass


class Color:
    pass


class Dict:
    pass


class Generic:
    pass


class Number:
    pass


class Float(Number):
    pass


class Integer(Number):
    pass


class ValueFloat(Float):
    pass


class ValueInterger(Integer):
    pass


def socket_type(t):
    return _type_dict[t]


_type_dict = {Color: "SvRxColorSocket",
              Dict: "SvRxDictSocket",
              Float: "SvRxFloatSocket",
              Generic: "SvRxGenericSocket",
              Integer: "SvRxIntSocket",
              Mesh: "SvRxMeshSocket",
              Number: "SvRxFloatSocket",
              String: "SvRxStringSocket",
              Topology: "SvRxTopologySocket",
              Vertices: "SvRxVerticesSocket",
              Vector: "SvRxVectorSocket",
              ValueInterger: "SvRxIntValueSocket",
              ValueFloat: "SvRxFloatValueSocket",
              }
