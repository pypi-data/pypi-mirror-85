import sys

from tbdump.__main__ import error
from tibidi.loader import load


def tbpeep():
    if len(sys.argv) != 2:
        error('Usage: tbpeep DUMPNAME', ExitCodes.USAGE_ERROR)
    filename = sys.argv[1]
    dump = load(filename)
    try:
        from peepshow import peep_
    except ImportError:
        error("Package 'peepshow' needs to be installed.", ExitCodes.DEPS_ERROR)
    peep_('dump')


if __name__ == '__main__':
    tbpeep()
