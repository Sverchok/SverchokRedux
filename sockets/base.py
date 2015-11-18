
class SvRxSocketBase(object):
    """base class for sockets """
    def serialize(self):
        socket_dict = {"name": self.name,
                       "bl_idname": self.bl_idname,
                       "default_value": getattr(self, "default_value", None),
                       "is_linked": self.is_linked
                       }
        return socket_dict

    def load(self, socket_dict):
        value = socket_dict["default_value"]
        if not value is None:
            self.default_value = value
