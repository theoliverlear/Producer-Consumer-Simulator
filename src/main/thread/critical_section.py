import functools
import logging
import threading

from src.main.thread.processor.lock.mutex_lock import MutexLock


def critical_section(function):
    """
    Decorator to apply a mutex lock for critical sections of code. This
    ensures that only one thread at a time can execute the decorated function,
     providing thread-safety.

    :param function: The function being wrapped by the decorator.
    :type function: Callable
    :return: A wrapper function that enforces thread-safe execution of the
    given function using a mutex lock.
    :rtype: Callable
    """
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        lock: MutexLock = self.mutex_lock
        thread_name: str = threading.current_thread().name
        logging.debug(f"Thread {thread_name} entering critical section in {function.__name__}.")
        with lock:
            result = function(self, *args, **kwargs)
        logging.debug(f"Thread {thread_name} exiting critical section in {function.__name__}.")
        return result
    return wrapper