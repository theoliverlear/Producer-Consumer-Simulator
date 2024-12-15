import time
from typing import List

from src.main.logging.logging_utilities import log_in_bold, \
    print_logging_seperator
from src.main.statistics.track_performance import nanoseconds_to_milliseconds, \
    format_execution_time_number


class StatisticTracker:
    """
    Tracks statistics for producer-consumer operations, including throughput
    and buffer state metrics.

    :ivar num_items_to_process: Total number of items the tracker expects
        to process.
    :type num_items_to_process: int
    :ivar producer_throughput_list: Records producer throughput values.
    :type producer_throughput_list: List[float]
    :ivar consumer_throughput_list: Records consumer throughput values.
    :type consumer_throughput_list: List[float]
    :ivar items_produced: Counter for items produced.
    :type items_produced: int
    :ivar items_consumed: Counter for items consumed.
    :type items_consumed: int
    :ivar num_empty_buffer: Counter for how many times the buffer was empty.
    :type num_empty_buffer: int
    :ivar num_full_buffer: Counter for how many times the buffer was full.
    :type num_full_buffer: int
    :ivar start_time: Time when tracking started.
    :type start_time: float
    :ivar end_time: Time when tracking stopped.
    :type end_time: float
    """
    def __init__(self,
                 num_items_to_process: int):
        """
        This class tracks the throughput and performance metrics for a
        producer-consumer system. It keeps record of throughput lists for
        producers and consumers, production and consumption counts, and buffer
         states.

        :param num_items_to_process: The total number of items to be produced
            and consumed in the system.
        :type num_items_to_process: int
        :ivar num_items_to_process: The number of items to process.
        :type num_items_to_process: int
        :ivar producer_throughput_list: List to hold throughput metrics for
            the producer.
        :type producer_throughput_list: List[float]
        :ivar consumer_throughput_list: List to hold throughput metrics for
            the consumer.
        :type consumer_throughput_list: List[float]
        :ivar items_produced: Number of items produced so far.
        :type items_produced: int
        :ivar items_consumed: Number of items consumed so far.
        :type items_consumed: int
        :ivar num_empty_buffer: Count of how many times the buffer was empty
            during the process.
        :type num_empty_buffer: int
        :ivar num_full_buffer: Count of how many times the buffer was full
            during the process.
        :type num_full_buffer: int
        :ivar start_time: The start time of the process.
        :type start_time: Any
        :ivar end_time: The end time of the process.
        :type end_time: Any
        """
        self.num_items_to_process: int = num_items_to_process
        self.producer_throughput_list: List[float] = []
        self.consumer_throughput_list: List[float] = []
        self.items_produced: int = 0
        self.items_consumed: int = 0
        self.num_empty_buffer: int = 0
        self.num_full_buffer: int = 0
        self.start_time: float = 0
        self.end_time: float = 0
    def start(self) -> None:
        """
        This method initializes the tracking mechanism for monitoring
        processes within the system.

        :return: None
        """
        self.start_tracking()

    def stop(self) -> None:
        """
        Stops the tracking process and displays the gathered statistics.

        :return: This method does not return any value.
        :rtype: None
        """
        self.stop_tracking()
        self.show_statistics()

    def increment_produced_items(self) -> None:
        """
        Increments the count of produced items.

        :return: This method does not return any value.
        :rtype: None
        """
        self.items_produced += 1

    def increment_consumed_items(self) -> None:
        """
        Increments the count of consumed items.

        :return: This method does not return any value.
        :rtype: None
        """
        self.items_consumed += 1

    def increment_empty_buffer(self) -> None:
        """
        Increments the value of `num_empty_buffer`.

        :return: This method does not return any value.
        :rtype: None
        """
        self.num_empty_buffer += 1

    def increment_full_buffer(self) -> None:
        """
        Increments the value of `num_full_buffer`.

        :return: None
        :rtype: None
        """
        self.num_full_buffer += 1

    def start_tracking(self) -> None:
        """
        Starts tracking time by recording the current time using the time
        module.

        :rtype: None
        :return: This method does not return any value.
        """
        self.start_time = time.time()

    def stop_tracking(self) -> None:
        """
        Stops the tracking process by recording the end time.

        :return: This method does not return any value.
        :rtype: None
        """
        self.end_time = time.time()

    def get_total_time(self) -> float:
        """
        Calculates the total time duration based on the difference between
        the object's end time and start time attributes.

        :return: The total duration as a float value.
        :rtype: float
        """
        return self.end_time - self.start_time

    def add_producer_throughput(self, throughput: float) -> None:
        """
        Adds the throughput value for a producer to the throughput list.

        :param throughput: The throughput value to be added, representing the
            production rate of a producer as a float.
        :return: This method does not return any value.
        :rtype: None
        """
        self.increment_produced_items()
        self.producer_throughput_list.append(throughput)

    def add_consumer_throughput(self, throughput: float) -> None:
        """
        Adds the throughput value for a producer to the throughput list.

        :param throughput: Throughput of the consumer to be added.
        :type throughput: float
        :return: This method does not return any value.
        :rtype: None
        """
        self.increment_consumed_items()
        self.consumer_throughput_list.append(throughput)

    def show_statistics(self) -> None:
        """
        Displays statistics related to buffer usage and system performance.

        This function outputs details such as buffer statistics and performance
        information. It leverages logging helpers for bold formatting and
        separator lines for improved readability.

        :return: None
        """
        print_logging_seperator()
        log_in_bold(self.get_buffer_statistics())
        print_logging_seperator()
        log_in_bold(self.get_performance_info())
        print_logging_seperator()

    def get_buffer_statistics(self) -> str:
        """
        Provides a summary of the buffer's usage statistics. It reports how
        many times the buffer was empty or full based on the recorded values.

        :return: A string containing formatted statistics about the buffer's
            usage.
        :rtype: str
        """
        buffer_statistics: str = f"""
        Number of times buffer was empty: {self.num_empty_buffer}
        Number of times buffer was full: {self.num_full_buffer}"""
        return buffer_statistics

    def get_performance_info(self) -> str:
        """
        Calculates and formats performance information for producer and consumer
        throughput. The method determines and converts time units based on the
        provided throughput values, ensuring appropriate time intervals are
        used either in nanoseconds or milliseconds.

        :return: A formatted string summarizing producer and consumer
        throughput in the appropriate time interval.
        :rtype: str
        """
        producer_throughput: float | int = self.get_average_throughput(self.producer_throughput_list)
        consumer_throughput: float | int = self.get_average_throughput(self.consumer_throughput_list)
        time_interval: str = 'nanoseconds'
        use_nanoseconds_threshold = 1_000_000
        should_use_milliseconds = (producer_throughput >
                                   use_nanoseconds_threshold or
                                   consumer_throughput >
                                   use_nanoseconds_threshold)
        if should_use_milliseconds:
            producer_throughput = nanoseconds_to_milliseconds(producer_throughput)
            consumer_throughput = nanoseconds_to_milliseconds(consumer_throughput)
            time_interval = 'milliseconds'
        producer_throughput_str: str = format_execution_time_number(producer_throughput)
        consumer_throughput_str: str = format_execution_time_number(consumer_throughput)
        performance_string: str = f"""
        Producer throughput: {producer_throughput_str} {time_interval} per item
        Consumer throughput: {consumer_throughput_str} {time_interval} per item"""
        return performance_string

    @staticmethod
    def get_average_throughput(throughput_list: List[float]) -> float:
        """
        Calculate and return the average throughput value from a given list of
        throughput values.

        :param throughput_list: A list of throughput values as floats.
        :type throughput_list: List[float]
        :return: The average throughput value as a float.
        """
        return sum(throughput_list) / len(throughput_list)