import functools
import time
import traceback
from tkinter import Event

from .base import *
from .console import pp




__all__ = ['Debug', 'ClassMethodDebug', 'CheckTime', 'CheckTimeWithSignature', 'DebugTkinterEvent', 'SimpleDebug', 'StackTrace', 'StackTraceWithSignature']

debug = __debug__

def ClassMethodDebug(cls: str or type, tag: str = DEFAULT_TAG):
    """
        Print the function signature and return value

    :param cls: class string or type to describe the method's parent or caller.
    :param tag: a unique string to identify the output in the console window.
    :return:
    """
    if isinstance(cls, type):
        cls = cls.__name__

    def debug_inner(func: callable = None):
        """
            Print the function signature and return value

        :param func: callable function to be debugged.
        :return:
        """
        name = f"{cls}.{func.__name__}"

        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            if debug:
                print(tag.format(name))
                if args or kwargs:
                    try: args_repr = [repr(a) for a in args]  # 1
                    except: args_repr = [str(a) for a in args]  # 1

                    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2

                    signature = ", ".join(args_repr + kwargs_repr)  # 3

                    print(f"{name}(\n      {signature}\n   )")
            result = func(*args, **kwargs)
            if debug: print(f"{name}  returned  {result!r}\n")  # 4

            return result
        return wrapper_debug
    return debug_inner



def Debug(func: callable, tag: str = DEFAULT_TAG):
    """
        Print the function signature and return value

    :param func: callable function to be debugged.
    :param tag: a unique string to identify the output in the console window.
    :return:
    """
    name = GetFunctionName(func)

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        if debug: print_signature(func, tag, *args, **kwargs)
        result = func(*args, **kwargs)
        if debug: print(f"{name}  returned  {result!r}\n")  # 4

        return result
    return wrapper_debug
def SimpleDebug(func: callable):
    """
        Print the function signature and return value

    :param func: callable function to be debugged.
    :return:
    """
    name = GetFunctionName(func)

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        if debug: print(f"--------- CALLED: {name}\n")
        result = func(*args, **kwargs)
        if debug: print(f"--------- ENDED: {name}\n")

        return result
    return wrapper_debug



def CheckClsTime(*, cls: str or type = None, printSignature: bool = True, tag: str = DEFAULT_TAG):
    """
        Print the function signature and return value

    :param printSignature:
    :param cls: class string or type to describe the method's parent or caller.
    :param tag: a unique string to identify the output in the console window.
    :return:
    """
    if isinstance(cls, type): cls = cls.__name__

    def timeit(func: callable):
        name = GetFunctionName(func)

        @functools.wraps(func)
        def timed(*args, **kwargs):
            if debug:
                print(tag.format(name))
                if printSignature:
                    try: args_repr = [repr(a) for a in args]  # 1
                    except: args_repr = [str(a) for a in args]  # 1

                    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2

                    signature = ", ".join(args_repr + kwargs_repr)  # 3

                    if cls is not None:
                        print(f"\n{cls}.{func.__name__}\n{signature}")
                    else:
                        print(f"\n{func.__name__}\n{signature}")

            start_time = time.time()
            result = func(*args, **kwargs)
            if debug:
                print(f'{name}  took  {time.time() - start_time}')
                print(f"{name}  returned  {result!r}\n")  # 4
            return result

        return timed
    return timeit

def RoundFloat(Float: float, Precision: int) -> str:
    """ Rounds the Float to the given Precision and returns It as string. """
    return f"{Float:.{Precision}f}"
def CheckTime(func: callable, Precision: int = 4):
    name = GetFunctionName(func)

    @functools.wraps(func)
    def timed(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        if debug:
            t = time.time() - start_time
            print(f'{name}  took:  {RoundFloat(t, Precision=Precision)}')
        return result

    return timed
def CheckTimeWithSignature(func: callable, Precision: int = 4, tag: str = DEFAULT_TAG):
    name = GetFunctionName(func)

    @functools.wraps(func)
    def timed(*args, **kwargs):
        print_signature(func, tag, *args, **kwargs)

        start_time = time.time()
        result = func(*args, **kwargs)
        if debug:
            t = time.time() - start_time
            print(f'{name}  took:  {RoundFloat(t, Precision=Precision)}')
            print(f"{name}  returned  {result!r}\n")
        return result

    return timed



def DebugTkinterEvent(func: callable, tag: str = DEFAULT_TAG):
    name = GetFunctionName(func)

    @functools.wraps(func)
    def wrapper_debug(self, event: Event, *args, **kwargs):
        if debug:
            print(tag.format(f'{name}'))
            print(f'{name}.{event.__class__}')
            pp.pprint(event.__dict__)

        result = func(self, event, *args, **kwargs)
        if debug: print(f"{name}  returned  {result!r}\n")

        return result

    return wrapper_debug



def StackTrace(func, INDENT=4 * ' '):
    """
        Get all but last line returned by traceback.format_stack() which is the line below.

    :param func:
    :type func:
    :param INDENT:
    :type INDENT:
    :return:
    :rtype:
    """
    name = GetFunctionName(func)

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if debug:
            callstack = '\n'.join([INDENT + line.strip() for line in traceback.format_stack()][:-1])
            print(f'{name}() called:')
            print(callstack)
        result = func(*args, **kwargs)
        if debug: print(f"{name}  returned  {result!r}\n")

    return wrapped
def StackTraceWithSignature(func, INDENT=4 * ' ', tag: str = DEFAULT_TAG):
    """
        Get all but last line returned by traceback.format_stack() which is the line below.

    :param tag:
    :type tag:
    :param func:
    :type func:
    :param INDENT:
    :type INDENT:
    :return:
    :rtype:
    """
    name = GetFunctionName(func)

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if debug:
            callstack = '\n'.join([INDENT + line.strip() for line in traceback.format_stack()][:-1])
            print_signature(func, tag, *args, **kwargs)
            print(callstack)
        result = func(*args, **kwargs)
        if debug: print(f"{name}  returned  {result!r}\n")

    return wrapped
