import logging
import queue
import time
import uuid

from concurrentevents.eventhandler import EventHandler
from concurrentevents.tools.threadmonitor import thread_monitor

logger = logging.getLogger('concurrentevents')


class ResourcePool:
    """
    Organizational tool used for resource load balancing with options for thread safety

    Uses carousel queue to balance loads between resources
    If it is specified to be thread_save additional resources are created to
    match the number of threads running and resource use it checked when
    requesting a resource

    Args:
        :param resource: An initialized resource object
        :type resource: class:`concurrentevents.Resource`
        :param amount: A number of resource to have in rotation
        :type amount: int
    Kwargs
        :param thread_safe: An option to require all resource and use to be thread safe
        :type thread_safe: bool, optional
    """
    def __init__(self, resource, amount, thread_safe=False):
        """Constructor Method"""
        try:
            if not (isinstance(resource, Resource) or issubclass(resource.__class__, Resource)):
                raise TypeError
        except TypeError:
            raise TypeError(
                f"ResourceManager() resource argument must be a "
                f"Resource or subclass of Resource, not {resource}")

        if not isinstance(amount, int):
            raise TypeError(f"ResourceManager() amount argument must be an int, not {amount}")

        if not isinstance(thread_safe, bool):
            raise TypeError(f"ResourceManager() amount argument must be a bool, not {thread_safe}")

        self.thread_safe = thread_safe

        self.__resources = queue.Queue()

        # Loop to copy a resource to populate __resources
        self.__resources.put(resource)
        for i in range(1, amount):
            self.__resources.put(resource.copy())

    @thread_monitor
    def get(self, timeout=0):
        """
        Returns a resource object from the queue of resources with a timeout

        Args:
            :param timeout: A timeout variable set to none to be used in the queue.get(timeout) function
            :type timeout: int, None, optional

        :return: One of the resource from the pool
        :rtype: class:`concurrentevents.Resource`
        """
        if not isinstance(timeout, int) or timeout < 0:
            raise ValueError("timeout must be an int greater than zero")

        res = self.__resources.get(timeout=timeout)
        self.__resources.put(res, timeout=timeout)

        if self.thread_safe:
            endtime = time.monotonic() + timeout
            while res._in_use:
                res = self.__resources.get(timeout=timeout)
                self.__resources.put(res, timeout=timeout)

                if timeout:
                    if endtime - time.monotonic() <= 0.0:
                        raise TimeoutError

                time.sleep(0.25)

        res._in_use = True
        return res


class Resource(EventHandler):
    """
    A generic class to wrap a function or class and allow it to be used in a resource pool

    Args:
        :param f: A function object to be pasted in for executions
        :type f: class:`function`
    """
    def __init__(self, f=None, **kwargs):
        """Constructor Method"""
        self._f = f
        self.id = uuid.uuid4()
        self._in_use = False
        self._kwargs = kwargs

        super().__init__(**kwargs)

    def copy(self):
        """
        A copy constructor to allow for duplicates to be made to populate the resource pool

        :return: A new instance of the same class
        """
        try:
            if issubclass(self.__class__, Resource) or isinstance(self, Resource):
                return self.__class__(self._f or None, **self._kwargs)
        except TypeError:
            return self.__class__()

    def __call__(self, *args, **kwargs):
        """
        Executes the stored function with args and keyword args

        Args:
            :param args: Arguments for the internal function
            :param kwargs: Keyword Arguments for the internal function

        :return: Returns any results from the function
        """
        return self._f(*args, **kwargs)

    def open(self):
        """
        Empty function to override if functionality wants to be
        added to the __enter__ operation
        """

    def close(self):
        """
        Function can either be override to add function to the with statement or
        if no with statement is used this signals that the object is no longer
        in use __exit__ operation
        """
        self._in_use = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._in_use = False
        self.close()
        if exc_type:
            logger.exception(exc_type)
            return False
        return True
