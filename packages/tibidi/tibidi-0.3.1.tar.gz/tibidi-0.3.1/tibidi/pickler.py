import io
import sys
from cloudpickle import CloudPickler, load, loads
from functools import lru_cache


class Dummy:
    def __init__(self, error):
        self._error = error

    def __str__(self):
        return f'<{type(self._error).__name__}: {self._error}>'


class Dispatcher:
    def __init__(self, data, protocol):
        self._data = data

    @lru_cache
    def __getitem__(self, type_):
        reduce_ = self._data[type_]
        if reduce_ is None:
            return None
        def reduce_safe(obj):
            try:
                return reduce_(obj)
            except Exception as exc:
                return (Dummy, (exc,), None, None, None, None)
        return reduce_safe


def CloudPicklerPermisiveFactory(protocol):
    class CloudPicklerPermisive(CloudPickler):
        dispatch = Dispatcher(CloudPickler.dispatch, protocol)
        dispatch_table = Dispatcher(CloudPickler.dispatch_table, protocol)
    return CloudPicklerPermisive

def dump(obj, fh, protocol=None):
    CloudPicklerPermisiveFactory(protocol)(fh, protocol=protocol).dump(obj)

def dumps(obj, protocol=None):
    with io.BytesIO() as fh:
        cp = CloudPicklerPermisiveFactory(protocol)(fh, protocol=protocol)
        cp.dump(obj)
        return fh.getvalue()

