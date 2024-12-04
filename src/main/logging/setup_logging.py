import functools
import logging
import threading
import time

def setup_logging(use_verbose: bool = False) -> None:
    if use_verbose:
        setup_verbose_logging()
    else:
        setup_default_logging()
def setup_default_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
        datefmt='%H:%M:%S'
    )

def setup_verbose_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
        datefmt='%H:%M:%S'
    )

def execution_trace(function):
    def wrapper(*args, **kwargs):
        thread_name: str = threading.current_thread().name
        logging.debug(f"Executing {function.__name__} on thread {thread_name}")
        result = function(*args, **kwargs)
        logging.debug(f"Finished executing {function.__name__} on thread {thread_name}")
        return result
    return wrapper


