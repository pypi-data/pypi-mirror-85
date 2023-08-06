import sys
import runpy
from tibidi import set_excepthook
from tibidi.loader import load
from tibidi.dumper import DEFAULT_DUMP_NAME, dump_exception
from enum import IntEnum

class ExitCodes(IntEnum):
    SUCCESSFUL = 0
    USAGE_ERROR = 1
    DEPS_ERROR = 2
    DUMPING_FAILED = 3


def error(text, exit_code):
    print(text, file=sys.stderr)
    exit(exit_code)


def tbdump():
    if len(sys.argv) < 2:
        error('Usage: tbdump PATH [ARGS...]', ExitCodes.USAGE_ERROR)
    filename = sys.argv[1]
    sys.argv = sys.argv[1:]
    try:
        runpy.run_path(filename, run_name='__main__')
    except Exception as exc:
        try:
            dump_exception(exc, DEFAULT_DUMP_NAME, start_from=filename)
            print(type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
            print('Traceback dumped into: ' + DEFAULT_DUMP_NAME, file=sys.stderr)
        except Exception as exc_inner:
            error(f'{type(exc_inner).__name__}: {exc_inner}', ExitCodes.DUMPING_FAILED)


if __name__ == '__main__':
    tbdump()
