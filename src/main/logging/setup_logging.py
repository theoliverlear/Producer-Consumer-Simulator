import functools
import logging
import threading
import time


def setup_logging(use_verbose: bool = False):
    logging.basicConfig(
        level=logging.DEBUG if use_verbose else logging.INFO,
        format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"
    )

def execution_trace(function):
    def wrapper(*args, **kwargs):
        thread_name: str = threading.current_thread().name
        logging.debug(f"Executing {function.__name__} on thread {thread_name}")
        result = function(*args, **kwargs)
        logging.debug(f"Finished executing {function.__name__} on thread {thread_name}")
        return result
    return wrapper

def performance_timing(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        thread_name: str = threading.current_thread().name
        start_time: float = time.perf_counter()
        result = function(*args, **kwargs)
        end_time: float = time.perf_counter()
        execution_time: float = end_time - start_time
        logging.debug(f"Execution time for {function.__name__} on thread {thread_name}: {execution_time:.4f} seconds")
        return result
    return wrapper
