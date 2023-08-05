from functools import wraps
import errno
import os
import signal


class TimeoutError(Exception):
    pass


def timeout(seconds=None, error_message=os.strerror(errno.ETIME)):
    """
    Decorator that raises TimeoutError if given time is exceeded.
    Args:
        seconds(int): time to wait until triggering the exception
        error_message(str)
    Examples:
        >>> import time
        >>> import w7x

        >>> def short_runtime():
        ...     print("Done")

        >>> def long_runtime():
        ...     time.sleep(2)
        ...     print("Done")

        No timeout
        >>> _ = w7x.lib.timeout.timeout(None)(short_runtime)()
        Done

        Timeout a long running function with the default expiry of 1 second.
        >>> _ = w7x.lib.timeout.timeout(1)(long_runtime)()  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TimeoutError: Timer expired

    """
    if seconds is None:
        seconds = 0

    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            if os.name == 'nt':  # signal.SIGALRM not existing under windows :/
                result = func(*args, **kwargs)
            else:
                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(seconds)
                try:
                    result = func(*args, **kwargs)
                finally:
                    signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


if __name__ == "__main__":
    import doctest
    doctest.testmod()
