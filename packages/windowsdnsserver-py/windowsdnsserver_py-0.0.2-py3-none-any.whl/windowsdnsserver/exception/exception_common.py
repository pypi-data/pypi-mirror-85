import inspect


class MethodNotImplementedError(RuntimeError):

    def __init__(self):
        clazz = inspect.stack()[1][0].f_locals.get('self', None).__class__.__name__
        method = inspect.stack()[1].function
        super(MethodNotImplementedError, self).__init__('%s.%s not implemented' % (clazz, method))

