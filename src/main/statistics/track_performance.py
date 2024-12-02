import functools
import logging
import threading
import time


def track_performance(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        thread_name: str = threading.current_thread().name
        start_time: float = time.perf_counter_ns()
        result = function(*args, **kwargs)
        end_time: float = time.perf_counter_ns()
        execution_time: int = int(end_time - start_time)
        logging.info(f"Execution time for {function.__name__} on thread {thread_name}: {execution_time} nanoseconds.")
        return result

    return wrapper
