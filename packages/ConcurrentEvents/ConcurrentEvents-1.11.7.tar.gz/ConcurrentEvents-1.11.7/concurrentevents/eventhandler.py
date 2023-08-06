from concurrentevents._exceptions import Cancel


class EventHandler:
    """
    The main class used to implement a function to handle an event

    This is not required to handle function but rather standardizes useful
    functionality to simplify implementation

    Args:
        :param `**kwargs`: Keyword arguments used to set member variables
    """
    event_manager = None

    def __init__(self, **kwargs):
        """Constructor Method"""
        for keyword, arg in kwargs.items():
            setattr(self, keyword, arg)

    @classmethod
    def fire(cls, event):
        """
        Wrapper function for the event manager fire function

        Allows for function under an implemented event handler class to fire new events

        Args:
            :param event: A event to be fired through the event manager
            :type event: class:`concurrentevents.Event`
        """
        cls.event_manager.fire(event)

    @staticmethod
    def cancel():
        """
        A shortcut function to raise the cancel error signaling the __handler function to stop
        :raises Cancel: This error is a shortcut to trigger changes in the handling of an event
        """
        raise Cancel()
