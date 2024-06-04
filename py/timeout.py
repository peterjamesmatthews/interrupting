import ctypes
import threading
from functools import wraps
from queue import Empty, Queue


def timeout(n: int):
    """
    timeout is a decorator that adds a timeout to a flask route.

    If the function takes more than n seconds to execute:
    - The decorator will return `("500 Server Timeout", 500)`.
    - The function will continue to execute in the background.

    Args:
        n (int): the timeout in seconds

    Returns:
        function: the decorated function
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Create a queue to store the result of the function
            result = Queue(1)

            # the target only puts the result of the function in the queue
            def target():
                result.put(f(*args, **kwargs))

            # start a thread to run the target
            threading.Thread(target=target).start()

            # get the result from the queue with a timeout
            try:
                return result.get(timeout=n)
            except Empty:
                return "Server Timeout", 500

        return wrapper

    return decorator


class TimeoutException(Exception): ...


def exceptional_timeout(n: int):
    """exceptional_timeout is a decorator that adds a timeout to a flask route.

    If the function takes more than n seconds to execute:
    - The decorator will return `("500 Server Timeout", 500)`.
    - The function will continue to execute in the background.
    - The thread running the function will have a TimeoutException raised in it.

    Args:
        n (int): the timeout in seconds

    Returns:
        function: the decorated function"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = Queue(1)

            def target():
                result.put(f(*args, **kwargs))

            t = threading.Thread(target=target)

            t.start()

            if t.ident is None:
                raise RuntimeError("Thread is not started")

            try:
                return result.get(timeout=n)
            except Empty:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(t.ident),
                    ctypes.py_object(TimeoutException),
                )
                return "Server Timeout", 500

        return wrapper

    return decorator
