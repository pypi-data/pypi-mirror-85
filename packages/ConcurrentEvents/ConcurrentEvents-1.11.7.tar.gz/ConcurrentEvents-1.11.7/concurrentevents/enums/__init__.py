from enum import Enum


class Priority(Enum):
    """
    Enum is used to order handlers for a specific event

    The idea is that each event is a thread so that in order
    to let certain handlers go before less important ones

    Example:

    .. highlight:: python
    .. code-block:: python

        @Catch(Start, Priority.CRITICAL)
        def foo():
            pass
    """
    CRITICAL = 0
    HIGH = 10
    MEDIUM = 20
    LOW = 30
    END = 40

    def __int__(self):
        return self.value
