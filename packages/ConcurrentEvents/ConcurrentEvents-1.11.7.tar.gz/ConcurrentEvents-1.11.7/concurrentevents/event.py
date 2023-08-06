class Event:
    """
    Basic Event Class

    This class is meant to be used as a superclass for specific event
    Those classes than inherit the Event class can now be used with @Catch(PrintEvent)
    and when fired to the event manager with handlers catching it will be run

    .. highlight:: python
    .. code-block:: python

        class PrintEvent(Event):
            def __init__(self, toprint)
                Event.__init__(self, toprint=toprint)

        class PrintHandler(EventHandler):
            @Catch(PrintEvent)
            def printAnything(toprint)
                print(toprint)

    Args:
        :param `*args`: Arguments for handling functions
        :param `**kwargs`: Keyword arguments for handling function
    """
    def __init__(self, *args, **kwargs):
        """Constructor Method"""
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """
        Created a string of an event

        >>>str(Start)
        'Start(args=(foo), kwargs={'foo':bar})'

        :return: A string of the event including args and kwargs
        :rtype: str
        """
        return f"{self.__class__.__name__}(args={self.args}, kwargs={self.kwargs})"


class Start(Event):
    """An implementation of the Event class to signal program start"""


class Exit(Event):
    """
    An implementation of the Event class to signal program exit

    Args:
        :param timeout: A timeout option for shutdown operations
        :type timeout: int, optional
    """
    def __init__(self, timeout=5):
        """Constructor Method"""
        self.timeout = timeout
        super().__init__()
