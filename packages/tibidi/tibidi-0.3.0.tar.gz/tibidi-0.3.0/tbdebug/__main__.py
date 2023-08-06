import sys

from tbdump.__main__ import error
from tibidi.loader import load

def examine(dump):
    __builtins__ = globals()['__builtins__']
    globals().clear()
    globals()['__builtins__'] = __builtins__
    del __builtins__
    breakpoint()


def tbdebug():
    if len(sys.argv) != 2:
        error('Usage: tbdebug DUMPNAME', ExitCodes.USAGE_ERROR)
    filename = sys.argv[1]
    dump = load(filename)
    examine(dump)


if __name__ == '__main__':
    tbdebug()
