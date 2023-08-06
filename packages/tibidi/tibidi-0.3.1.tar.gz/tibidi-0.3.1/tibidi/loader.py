import sys
import types
import tibidi.pickler as pickler
from contextlib import contextmanager
from tibidi.dumper import DEFAULT_DUMP_NAME


class ModuleStub(types.ModuleType):
    def __init__(self, fullname):
        super().__init__(fullname)
        self.__file__ = '<virtual>'
        self.__name__ = fullname
        self.__loader__ = self

    def __getattr__(self, name):
        return ModuleStub(f'{self.__name__}.{name}')

    def __iter__(self):
        yield from ()


class ModuleStubFinder:

    def find_module(self, fullname, path=None):
        return self

    def load_module(self, fullname):
            m = ModuleStub(fullname)
            sys.modules[fullname] = m
            return m


@contextmanager
def DummyModuleFactory():
    sys.meta_path.append(ModuleStubFinder())
    try:
        yield
    finally:
        sys.meta_path.pop()


def load(filename: str = DEFAULT_DUMP_NAME) -> dict:
    """Load crash information from a dump file.

    Arguments:
        filename: File name or path to be loded.

    Returns:
        Crash information.
    """
    with DummyModuleFactory():
        with open(filename, 'rb') as f:
            return pickler.load(f)

