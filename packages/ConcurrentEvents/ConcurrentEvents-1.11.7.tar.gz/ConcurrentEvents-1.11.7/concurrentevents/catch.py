from functools import wraps

from concurrentevents.enums import Priority
from concurrentevents.event import Event


def catch(event, priority=Priority.MEDIUM):
    """
    This is a decorator for adding member variables to a function
    that should be a handler of a specific event

    .. highlight:: python
    .. code-block:: python

        class ExampleHandler(EventHandler):

            @Catch(Start)
            def handleStart():
                foo()

            @Catch("Start")
            def handleStartFromString():
                bar()

            @Catch(Exit, priority=Priority.CRITICAL)
            def handleExitWithCriticalPriority():
                pass

    Args:
        :param event: Takes in a representation of an event
        :type event: str, class:`concurrentevents.Event`
    Kwargs:
        :param priority: An argument used to signal order to handlers for a specific event
        :type priority: class:`concurrentevents.Priority`, optional

    :raises TypeError: If any unaccepted values are passed in for either argument
    """
    try:
        if isinstance(event, str):
            evt = event
        elif issubclass(event, Event):
            evt = event.__name__
        else:
            raise TypeError
    except TypeError:
        raise TypeError(f"Catch() event argument must be an event or string, not {event}")

    try:
        prt = int(priority)
    except TypeError:
        raise TypeError(f"Catch() priority argument must be convertible to an int, not {priority}")

    def decorator(func):
        func.event = evt
        func.priority = prt

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    return decorator
