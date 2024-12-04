import functools
import logging
import threading
import time

from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.buffer.full_buffer_exception import FullBufferException


def track_performance(function):
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
        logging.info(f"Execution time for {function.__name__} on thread {thread_name}: {execution_time_str} {time_interval}.")
        return result

    return wrapper

def format_execution_time_number(execution_time: float | int) -> str:
    if isinstance(execution_time, int):
        return f"{execution_time:,}"
    else:
        return f"{execution_time:,.4f}"

def track_producer_performance(function):
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
        logging.info(f"Execution time for {function.__name__} on thread {thread_name}: {execution_time_str} {time_interval}.")
        return result
    return wrapper

def track_consumer_performance(function):
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
        logging.info(f"Execution time for {function.__name__} on thread {thread_name}: {execution_time_str} {time_interval}.")
        return result
    return wrapper

def track_exceptions(function):
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
    return int(milliseconds * 1000000)

def nanoseconds_to_milliseconds(nanoseconds: int | float) -> float:
    return nanoseconds / 1000000