from ..nodes import register_node


def node_script(*args, **values):
    def real_node_func(func):
        def annotate(func):
            for key, value in values.items():
                setattr(func, key, value)
            return func
        annotate(func)
        register_node(func, register_new=True)
        return func
    if args and callable(args[0]):
        return real_node_func(args[0])
    else:
        return real_node_func


def node_func(*args, **values):
    def real_node_func(func):
        def annotate(func):
            for key, value in values.items():
                setattr(func, key, value)
            return func
        annotate(func)
        register_node(func)
        return func
    if args and callable(args[0]):
        return real_node_func(args[0])
    else:
        return real_node_func
