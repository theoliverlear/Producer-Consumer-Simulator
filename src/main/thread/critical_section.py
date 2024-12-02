import functools
import logging
import threading


def critical_section(function):
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        lock = self.mutex_lock
        thread_name: str = threading.current_thread().name
        logging.debug(f"Thread {thread_name} entering critical section in {function.__name__}.")
        with lock:
            result = function(self, *args, **kwargs)
        logging.debug(f"Thread {thread_name} exiting critical section in {function.__name__}.")
        return result
    return wrapper