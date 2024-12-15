import functools
import logging
import threading
import time

from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.buffer.full_buffer_exception import FullBufferException


def track_performance(function):
    """
    Tracks the execution time of the given function and logs it with
    additional information, such as the thread name and formatted time
    string. If execution time is less than 1 millisecond, it converts
    the duration to nanoseconds and logs it accordingly.

    :param function: The function whose execution time is to be tracked.
    :type function: Callable
    :return: A wrapped function that tracks execution time when invoked.
    :rtype: Callable
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        thread_name: str = threading.current_thread().name
        start_time: float = time.perf_counter()  * 1000
        result = function(*args, **kwargs)
        end_time: float = time.perf_counter() * 1000
        execution_time: float | int = end_time - start_time
        time_interval: str = 'milliseconds'
        if execution_time < 1:
            execution_time = milliseconds_to_nanoseconds(execution_time)
            time_interval = 'nanoseconds'
        execution_time_str: str = format_execution_time_number(execution_time)
        logging.debug(f"Execution time for {function.__name__} on thread "
                      f"{thread_name}: {execution_time_str} {time_interval}.")
        return result
    return wrapper

def format_execution_time_number(execution_time: float | int) -> str:
    """
    Formats the given execution time number to include commas as
    thousands separators. For integer values, the output is formatted
    with commas and no decimals. For floating-point numbers, it formats
    up to four digits after the decimal place.

    :param execution_time: The execution time as either an integer
        (e.g., nanoseconds) or a float (e.g., milliseconds with decimals).
    :type execution_time: float | int
    :return: A formatted string representation of the execution time
        with appropriate separators and precision.
    :rtype: str
    """
    if isinstance(execution_time, int):
        return f"{execution_time:,}"
    else:
        return f"{execution_time:,.4g}"

def track_producer_performance(function):
    """
    A decorator that measures the execution time of a function called within
    a producer thread, logs its details, and tracks performance metrics.

    :param function: Function to be wrapped and monitored by the
        decorator.
    :type function: Callable
    :return: The decorated function with added performance tracking and
        logging logic.
    :rtype: Callable
    """
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        thread_name: str = threading.current_thread().name
        start_time: float = time.perf_counter() * 1000
        result = function(self, *args, **kwargs)
        end_time: float = time.perf_counter() * 1000
        execution_time: float | int = end_time - start_time
        nano_execution_time: int = milliseconds_to_nanoseconds(execution_time)
        time_interval: str = 'milliseconds'
        if execution_time < 1:
            execution_time = nano_execution_time
            time_interval = 'nanoseconds'
        self.statistic_tracker.add_producer_throughput(nano_execution_time)
        execution_time_str: str = format_execution_time_number(execution_time)
        logging.debug(f"Execution time for {function.__name__} on thread "
                      f"{thread_name}: {execution_time_str} {time_interval}.")
        return result
    return wrapper

def track_consumer_performance(function):
    """
    A decorator that measures the execution time of a function called within
    a consumer thread, logs its details, and tracks performance metrics.

    :param function: Function to be wrapped and monitored by the
        decorator.
    :type function: Callable
    :return: The decorated function with added performance tracking and
        logging logic.
    :rtype: Callable
    """
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        thread_name: str = threading.current_thread().name
        start_time: float = time.perf_counter() * 1000
        result = function(self, *args, **kwargs)
        end_time: float = time.perf_counter() * 1000
        execution_time: float | int = end_time - start_time
        nano_execution_time: int = milliseconds_to_nanoseconds(execution_time)
        time_interval: str = 'milliseconds'
        if execution_time < 1:
            execution_time = nano_execution_time
            time_interval = 'nanoseconds'
        self.statistic_tracker.add_consumer_throughput(nano_execution_time)
        execution_time_str: str = format_execution_time_number(execution_time)
        logging.debug(f"Execution time for {function.__name__} on thread "
                      f"{thread_name}: {execution_time_str} {time_interval}.")
        return result
    return wrapper

def track_exceptions(function):
    """
    A decorator function used to wrap a function and track specific
    exceptions. The decorator increments the corresponding counters
    in the statistic tracker when exceptions are caught.

    :param function: The function to be wrapped by the decorator.
    :type function: Callable
    :return: The wrapped function with exception tracking logic.
    :rtype: Callable
    """
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        try:
            result = function(self, *args, **kwargs)
            return result
        except FullBufferException:
            self.statistic_tracker.increment_full_buffer()
            raise
        except EmptyBufferException:
            self.statistic_tracker.increment_empty_buffer()
            raise
    return wrapper

def milliseconds_to_nanoseconds(milliseconds: float | int) -> int:
    """
    Converts the given time in milliseconds to nanoseconds.

    :param milliseconds: Time duration in milliseconds to be converted.
        Can be a float or an integer.
    :type milliseconds: float | int
    :return: The equivalent time duration in nanoseconds as an integer.
    :rtype: int
    """
    return int(milliseconds * 1000000)

def nanoseconds_to_milliseconds(nanoseconds: int | float) -> float:
    """
    Converts a time duration from nanoseconds to milliseconds. This
    function accepts either an integer or float representing the number of
    nanoseconds and returns the equivalent duration in milliseconds.

    :param nanoseconds: Time duration in nanoseconds to be converted.
    :type nanoseconds: int | float
    :return: Converted time duration in milliseconds.
    :rtype: float
    """
    return nanoseconds / 1000000