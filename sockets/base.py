
class SvRxSocketBase(object):
    """base class for sockets """
    def serialize(self):
        socket_dict = {"name": self.name,
                       "bl_idname": self.bl_idname,
                       "default_value": getattr(self, "default_value", None),
                       "is_linked": self.is_linked
                       }
        return socket_dict
