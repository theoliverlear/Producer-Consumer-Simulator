import logging
import time
from typing import List

from src.main.logging.logging_utilities import log_in_bold
from src.main.statistics.track_performance import nanoseconds_to_milliseconds, \
    format_execution_time_number


class StatisticTracker:
    def __init__(self,
                 num_items_to_process: int):
        self.num_items_to_process = num_items_to_process
        self.producer_throughput_list = []
        self.consumer_throughput_list = []
        self.items_produced = 0
        self.items_consumed = 0
        self.num_empty_buffer = 0
        self.num_full_buffer = 0
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_tracking()

    def stop(self):
        self.stop_tracking()
        self.show_statistics()

    def increment_produced_items(self):
        self.items_produced += 1

    def increment_consumed_items(self):
        self.items_consumed += 1

    def increment_empty_buffer(self):
        self.num_empty_buffer += 1

    def increment_full_buffer(self):
        self.num_full_buffer += 1

    def start_tracking(self):
        self.start_time = time.time()

    def stop_tracking(self):
        self.end_time = time.time()

    def get_total_time(self):
        return self.end_time - self.start_time
    def add_producer_throughput(self, throughput: float):
        self.increment_produced_items()
        self.producer_throughput_list.append(throughput)

    def add_consumer_throughput(self, throughput: float):
        self.increment_consumed_items()
        self.consumer_throughput_list.append(throughput)

    def print_logging_seperator(self):
        logging_seperator: str = "\n" + "-" * 60
        logging.info(logging_seperator)

    def show_statistics(self):
        self.print_logging_seperator()
        log_in_bold(self.get_buffer_statistics())
        self.print_logging_seperator()
        log_in_bold(self.get_performance_info())
        self.print_logging_seperator()

    def get_buffer_statistics(self):
        empty_to_item_ratio = self.num_empty_buffer / self.num_items_to_process
        full_to_item_ratio = self.num_full_buffer / self.num_items_to_process
        buffer_statistics = f"""
        Number of times buffer was empty: {self.num_empty_buffer} - {empty_to_item_ratio}:1 item
        Number of times buffer was full: {self.num_full_buffer} - {full_to_item_ratio}:1 item"""
        return buffer_statistics

    def get_performance_info(self):
        producer_throughput: float | int = self.get_average_throughput(self.producer_throughput_list)
        consumer_throughput: float | int = self.get_average_throughput(self.consumer_throughput_list)
        time_interval = 'nanoseconds'
        if producer_throughput > 1_000_000 or consumer_throughput > 1_000_000:
            producer_throughput = nanoseconds_to_milliseconds(producer_throughput)
            consumer_throughput = nanoseconds_to_milliseconds(consumer_throughput)
            time_interval = 'milliseconds'
        producer_throughput_str: str = format_execution_time_number(producer_throughput)
        consumer_throughput_str: str = format_execution_time_number(consumer_throughput)
        performance_string = f"""
        Producer throughput: {producer_throughput_str} {time_interval} per item
        Consumer throughput: {consumer_throughput_str} {time_interval} per item"""
        return performance_string


    @staticmethod
    def get_average_throughput(throughput_list: List[float]) -> float:
        return sum(throughput_list) / len(throughput_list)