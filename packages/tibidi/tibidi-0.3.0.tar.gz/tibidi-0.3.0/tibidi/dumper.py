import os
import sys
import types
import datetime
import tibidi.pickler as pickler

DEFAULT_DUMP_NAME = 'traceback.pkl'

class NotPickleable:
    def __init__(self, value):
        self._type_name = type(value).__name__

    def __repr__(self):
        return f'<{self._type_name}>'


class ExceptionInfo(list):

    def __repr__(self):
        return f'{self.type.__name__}: {self.str}'


class FrameInfo(dict):
    def __init__(self, filename, lineno, func_name, code_line):
        self._filename = filename
        self._lineno = lineno
        self._func_name = func_name
        self._code_line = code_line

    def __repr__(self):
        return f'{self._code_line}  # {self._func_name}[{self._filename}:{self._lineno}]'


def set_excepthook(filename: str = DEFAULT_DUMP_NAME, replace: bool = True,
                   silent: bool = False) -> None:
    """Install tbdump as an exception handler.

    Arguments:
        filename: File name or path to the dump file.
        replace: Set `False` to call original exception handler after tbdump.
        silent: Set `True` to suppress messages.
    """

    old_excepthook = sys.excepthook

    if silent:
        say = lambda text: None
    else:
        say = lambda text: print(text, file=sys.stderr)

    def tbdump_except_hook(exctype, exc, traceback):
        say(exctype.__name__ + ': ' + str(exc))
        try:
            dump_exception(exc, filename)
            say('Traceback dumped into: ' + filename)
        except Exception:
            if int(os.getenv('TBDUMP_DEBUG', '0')):
                raise
            say('Failed to dump traceback')

        if not replace:
            old_excepthook(exctype, exc, traceback)

    sys.excepthook = tbdump_except_hook


def dump_exception(exc: Exception, filename: str = DEFAULT_DUMP_NAME,
                   start_from: str = None) -> None:
    """Dump exception object and corresponding crash information into a file.

    Arguments:
        exc: Exception object with traceback.
        filename: Target file name or path.
        start_from: Name of the source file to be considered as topmost.
    """

    report = report_header()
    report['exceptions'] = exception_stack_info(exc)
    if start_from:
        last_exc = report['exceptions'][-1]
        while last_exc:
            if last_exc[0]._filename == start_from:
                break
            del last_exc[0]

    with open(filename, 'wb') as f:
        pickler.dump(report, f)


def report_header():
    system = {}
    system['sys.version'] = sys.version
    system['os.name'] = os.name
    system['os.uname'] = os.uname()
    info = {}
    info['timestamp'] = datetime.datetime.now().isoformat()
    info['system'] = system
    return info


def exception_stack_info(bottom_exc):
    info = []
    exc = bottom_exc
    while exc:
        info.append(exception_info(exc))
        if exc.__cause__ is None:
            if exc.__suppress_context__:
                exc = None
            else:
                exc = exc.__context__
        else:
            exc = exc.__cause__

    return info[::-1]


def exception_info(exc):
    info = ExceptionInfo()
    info.type = type(exc)
    info.str = str(exc)
    info.args = exc.args

    exc_tb = exc.__traceback__
    while exc_tb:
        info.append(frame_info(exc_tb.tb_frame, lineno=exc_tb.tb_lineno))
        exc_tb = exc_tb.tb_next

    return info


def frame_info(frame, lineno=None):
    if lineno is None:
        lineno = frame.f_lineno

    try:
        with open(frame.f_code.co_filename) as f:
            code_line = f.readlines()[lineno-1].strip()
    except Exception:
        raise
        code_line = '<unavailable code>'

    info = FrameInfo(filename=frame.f_code.co_filename,
                     lineno=lineno,
                     func_name=frame.f_code.co_name,
                     code_line=code_line)
    info.update(prepare_vars(frame.f_globals))
    info.update(prepare_vars(frame.f_locals))

    return info


def prepare_vars(all_vars):
    illegal_types = (types.FrameType, types.GeneratorType, types.TracebackType)
    is_pickleable = lambda value: not isinstance(value, illegal_types)
    is_dunder = lambda name: name.startswith('__') and name.endswith('__')
    load = {name: value for name, value in all_vars.items() if not is_dunder(name)}
    for name, value in load.items():
        if not is_pickleable(value):
            load[name] = NotPickleable(value)
    return load
