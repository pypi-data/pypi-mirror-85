from windowsdnsserver.exception.exception_common import MethodNotImplementedError


class Command(object):

    def build(self):
        raise MethodNotImplementedError()


class CommandRunner(object):

    def run(self, cmd: Command):
        raise MethodNotImplementedError()


class Result(object):

    def __init__(self, success: bool, code: int, out: str, err: str):
        self.success = success
        self.code = code
        self.out = out
        self.err = err
