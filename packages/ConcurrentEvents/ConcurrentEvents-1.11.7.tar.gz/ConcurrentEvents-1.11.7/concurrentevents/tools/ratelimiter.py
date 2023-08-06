import functools
import logging
import threading
import time
from concurrent.futures import thread

logger = logging.getLogger('concurrentevents')

limited = set()


def rate_limiter(limit, seconds):
    def handlerfunc(func):
        return RateLimiter(func=func, limit=limit, seconds=seconds)
    return handlerfunc


class RateLimiter:
    """
    This is an implementation of the Generic Cell Rate Algorithm which allows
    for rate limiting of function calls without the need for outside interaction

    Wikipedia: https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm

    :param limit: The maximum amount of calls acceptable for the period
    :param seconds: The period at which the limit is applied to. Default 1
    :return:
    """
    def __init__(self, func, limit, seconds=1):
        if limit < 0 if isinstance(limit, int) else False:
            raise ValueError(f"rate_limiter() limit argument must be an int greater than 0, not {limit}")

        if seconds < 0 if isinstance(seconds, int) else False:
            raise ValueError(f"rate_limiter() period argument must be an int greater than 0, not {seconds}")

        self.func = func
        functools.update_wrapper(self, func)

        self.lock = threading.Lock()

        # Do setup for variables for this specific decoration
        self.last_check = time.monotonic()
        self.limit = limit
        self.seconds = seconds
        self.interval = seconds / limit

        self.name = f"{func.__module__.split('.')[-1]}.{func.__name__}()"

    def __call__(self, *args, **kwargs):
        if thread._shutdown is True:
            return

        t = time.monotonic()  # Represents the time of the function call

        with self.lock:
            tat = max(self.last_check, t)  # Theoretical Arrival Time

            # Is the time for this to arrive less than the window for it
            if tat - t <= self.seconds - self.interval:

                # Push back the arrival time
                new_tat = max(tat, t) + self.interval
                self.last_check = new_tat

            # The time to arrive isn't within the window
            else:
                limited.add(self.name)
                sleep_time = self.interval
                logger.debug(f"{self.name} rate limiter sleeping for {sleep_time}")
                time.sleep(sleep_time)
                limited.remove(self.name)

        return self.func(*args, **kwargs)
