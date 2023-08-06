import collections
from functools import wraps

monitoring = collections.defaultdict(lambda: 0)


def thread_monitor(func):
    """
    This is a debug tool for tracking thread activity by specific key or function
    It can be used as both a decorator and in a with statement to monitor a
    specific segment of code

    After implementation information is stored in the monitoring default
    dictionary and will be logged through the event manager or can be printed

    Implementation as a decorator is as follows and will automatically generate
    a key based on the function information

    .. highlight:: python
    .. code-block:: python

        @thread_monitor
        def foo(bar):
            pass

    Using this in a with statement requires a key to distinguish the specific
    with statement across multiple threads

    .. highlight:: python
    .. code-block:: python

        def foo(bar):
            with thread_monitor("Foo"):
                pass

    :param func:
    :return:
    """
    class _Monitor:
        def __init__(self, key):
            self.key = key

        def __enter__(self):
            monitoring[self.key] += 1

        def __exit__(self, exc_type, exc_val, exc_tb):
            monitoring[self.key] -= 1
            if exc_val:
                raise exc_val

    if not callable(func):
        return _Monitor(func)

    monitor = _Monitor(f"{func.__module__.split('.')[-1]}.{func.__name__}()")

    @wraps(func)
    def wrapper(*args, **kwargs):
        with monitor:
            result = func(*args, **kwargs)
        return result
    return wrapper



