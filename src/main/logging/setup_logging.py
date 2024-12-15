import logging
import threading


def setup_logging(use_verbose: bool = False) -> None:
    """
    Sets up the logging configuration for the application. Depending on the
    provided ``use_verbose`` parameter, it will configure either verbose or
    default logging settings.

    :param use_verbose: A boolean indicating whether verbose logging
        should be enabled. If False, default logging will be used.
    :type use_verbose: bool
    :return: This function does not return a value.
    :rtype: None
    """
    if use_verbose:
        setup_verbose_logging()
    else:
        setup_default_logging()
def setup_default_logging() -> None:
    """
    Sets up the default logging configuration.

    This function configures the logging module to use a default logging
    setup with the INFO level. The message format includes timestamp, thread
    name, log level, and the log message. The timestamp is formatted to only
    show hours, minutes, and seconds.

    :return: None
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
        datefmt='%H:%M:%S'
    )

def setup_verbose_logging():
    """
    Sets up verbose logging configuration for the application.

    This function configures the logging module to use a default logging
    setup with the DEBUG level. The message format includes timestamp, thread
    name, log level, and the log message. The timestamp is formatted to only
    show hours, minutes, and seconds.

    :return: None
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
        datefmt='%H:%M:%S'
    )

def execution_trace(function):
    """
    A decorator that logs the execution details of a function, including its
    name and the thread on which it is executed.

    :param function: The function to be wrapped and logged.
    :type function: Callable
    :return: A wrapper function that logs execution details and calls the
        original function.
    :rtype: Callable
    """
    def wrapper(*args, **kwargs):
        thread_name: str = threading.current_thread().name
        logging.debug(f"Executing {function.__name__} on thread {thread_name}")
        result = function(*args, **kwargs)
        logging.debug(f"Finished executing {function.__name__} on thread {thread_name}")
        return result
    return wrapper


