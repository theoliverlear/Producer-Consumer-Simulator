from typing import Tuple


class Config:
    """
    Configuration class for managing and storing parameters related to a
    producer-consumer problem.

    This class encapsulates the configuration settings needed to control
    the behavior of producers, consumers, buffer size, and other operational
    parameters. It provides a structured way to handle various configurable
    aspects such as speed range, verbosity, and suggestions.

    :ivar buffer_size: The maximum number of items that can be stored in the
    buffer.
    :type buffer_size: int
    :ivar num_items_to_process: Total number of items to be produced and
        consumed by the system.
    :type num_items_to_process: int
    :ivar num_producers: Number of producer threads to actively produce items.
    :type num_producers: int
    :ivar num_consumers: Number of consumer threads to actively consume items.
    :type num_consumers: int
    :ivar consumer_speed_range: A tuple defining the range of speeds at which
    consumers operate.
    :type consumer_speed_range: Tuple[int, int]
    :ivar producer_speed_range: A tuple defining the range of speeds at which
    producers operate.
    :type producer_speed_range: Tuple[int, int]
    :ivar verbose: A flag indicating whether detailed logs or outputs
        should be enabled.
    :type verbose: bool
    :ivar suggestions: A flag indicating whether additional recommendations
        or suggestions are shown during program execution.
    :type suggestions: bool
    """
    def __init__(self,
                 buffer_size: int,
                 num_items_to_process: int,
                 num_producers: int,
                 num_consumers: int,
                 consumer_speed_range: Tuple[int, int],
                 producer_speed_range: Tuple[int, int],
                 verbose: bool,
                 suggestions: bool):
        """
        Constructor for initializing the class with configurable parameters to
        define a producer-consumer system. These parameters include buffer
        size, number of producers and consumers, the range for producer and
        consumer speeds, and configuring verbosity and suggestions features.

        :parameter buffer_size: The maximum size of the buffer.
        :type buffer_size: int
        :parameter num_items_to_process: An integer representing the total
        number of items to be processed by producers and consumers.
        :type num_items_to_process: int
        :parameter num_producers: An integer indicating the number of producer
            threads in the system.
        :type num_producers: int
        :parameter num_consumers: An integer indicating the number of consumer
            threads in the system.
        :type num_consumers: int
        :parameter consumer_speed_range: A tuple of two integers defining the
        range (in milliseconds) of processing speed for consumers.
        :type consumer_speed_range: Tuple[int, int]
        :parameter producer_speed_range: A tuple of two integers defining the
        range (in milliseconds) of processing speed for producers.
        :type producer_speed_range: Tuple[int, int]
        :parameter verbose: A boolean flag to control verbose output for
        debugging or logging purposes.
        :type verbose: bool
        :parameter suggestions: A boolean option to enable or disable
        suggestions for potential improvements in the system during runtime.
        :type suggestions: bool
        """
        self.buffer_size: int = buffer_size
        self.num_items_to_process: int = num_items_to_process
        self.num_producers: int = num_producers
        self.num_consumers: int = num_consumers
        self.consumer_speed_range: tuple[int, int] = consumer_speed_range
        self.producer_speed_range: tuple[int, int] = producer_speed_range
        self.verbose: bool = verbose
        self.suggestions: bool = suggestions

    def __str__(self):
        """
        Generates a formatted string representation of the instance.

        :return: A formatted string containing the instance attribute details.
        :rtype: str
        """
        return (f"Config(buffer_size={self.buffer_size},"
                f" num_items_to_process={self.num_items_to_process},"
                f" num_producers={self.num_producers},"
                f" num_consumers={self.num_consumers},"
                f" consumer_speed_range={self.consumer_speed_range},"
                f" producer_speed_range={self.producer_speed_range},"
                f" verbose={self.verbose}, suggestions={self.suggestions})")