class EventError(Exception):
    """Standard Event Exception"""


class Cancel(EventError):
    """Raised when an event is canceled"""


class StartError(EventError):
    """Raised when there is an error with starting the event manager"""
