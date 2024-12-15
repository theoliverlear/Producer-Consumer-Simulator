import logging
import random
import threading
from typing import List, Tuple

from src.main.buffer.buffer import Buffer
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.thread.processor.consumer.consumer import Consumer
from src.main.thread.processor.producer.producer import Producer


class ThreadManager:
    """
    Manages the creation, initialization, and synchronization of producer and
    consumer threads for processing items in a shared buffer.

    :ivar buffer: Shared buffer where producers add items and consumers remove
    them.
    :type buffer: Buffer
    :ivar num_items_to_process: Total number of items to be processed.
    :type num_items_to_process: int
    :ivar num_producers: Number of producer threads.
    :type num_producers: int
    :ivar num_consumers: Number of consumer threads.
    :type num_consumers: int
    :ivar producer_speed_range: Range of speeds for producers (min, max).
    :type producer_speed_range: Tuple[int, int]
    :ivar consumer_speed_range: Range of speeds for consumers (min, max).
    :type consumer_speed_range: Tuple[int, int]
    :ivar statistic_tracker: Tracker for monitoring and recording statistics.
    :type statistic_tracker: StatisticTracker
    :ivar threads_started: Indicator whether threads have been started.
    :type threads_started: bool
    :ivar producers: List of initialized producer threads.
    :type producers: List[Producer]
    :ivar consumers: List of initialized consumer threads.
    :type consumers: List[Consumer]
    """
    def __init__(self, num_producers: int,
                 num_consumers: int,
                 consumer_speed_range: Tuple[int, int],
                 producer_speed_range: Tuple[int, int],
                 buffer: Buffer,
                 num_items_to_process: int,
                 statistic_tracker: StatisticTracker):
        """
        This class initializes the producers and consumers based on the
        provided configuration and handles their interactions with the buffer
        for a given number of items.

        :param num_producers: Number of producer threads to create.
        :type num_producers: int
        :param num_consumers: Number of consumer threads to create.
        :type num_consumers: int
        :param consumer_speed_range: Speed range (min, max) for consumers.
        :type consumer_speed_range: Tuple[int, int]
        :param producer_speed_range: Speed range (min, max) for producers.
        :type producer_speed_range: Tuple[int, int]
        :param buffer: Shared buffer object between producers and consumers.
        :type buffer: Buffer
        :param num_items_to_process: Total number of items to be processed by the system.
        :type num_items_to_process: int
        :param statistic_tracker: Tracker for collecting processing statistics.
        :type statistic_tracker: StatisticTracker

        :ivar buffer: A shared buffer for producers and consumers to exchange
        data.
        :type buffer: Buffer
        :ivar num_items_to_process: The total number of items to be processed.
        :type num_items_to_process: int
        :ivar num_producers: The total number of producer threads.
        :type num_producers: int
        :ivar num_consumers: The total number of consumer threads.
        :type num_consumers: int
        :ivar producer_speed_range: Speed range (min, max) for producers.
        :type producer_speed_range: Tuple[int, int]
        :ivar consumer_speed_range: Speed range (min, max) for consumers.
        :type consumer_speed_range: Tuple[int, int]
        :ivar statistic_tracker: Tracks and collects performance statistics.
        :type statistic_tracker: StatisticTracker
        :ivar threads_started: Indicates whether the threads have been
        started.
        :type threads_started: bool
        :ivar producers: List of initialized producer instances.
        :type producers: List[Producer]
        :ivar consumers: List of initialized consumer instances.
        :type consumers: List[Consumer]
        """
        self.buffer: Buffer = buffer
        self.num_items_to_process: int = num_items_to_process
        self.num_producers: int = num_producers
        self.num_consumers: int = num_consumers
        self.producer_speed_range: tuple[int, int] = producer_speed_range
        self.consumer_speed_range: tuple[int, int] = consumer_speed_range
        self.statistic_tracker: StatisticTracker = statistic_tracker
        self.threads_started: bool = False
        self.producers: List[Producer] = self.initialize_producers()
        self.consumers: List[Consumer] = self.initialize_consumers()

    def initialize_producers(self) -> List[Producer]:
        """
        Initializes and returns a list of Producer objects.

        :return: A list of initialized Producer objects.
        :rtype: List[Producer]
        """
        items_per_producer, leftover_items = self.get_num_items_to_produce()
        producers: List[Producer] = []
        for i in range(self.num_producers):
            items_to_produce: int = items_per_producer + (1 if i < leftover_items else 0)
            producers.append(Producer(i + 1,
                                      self.producer_speed_range[0],
                                      self.producer_speed_range[1],
                                      self.buffer,
                                      items_to_produce,
                                      self.statistic_tracker))
            logging.debug(f"Producer {i + 1} will produce {items_to_produce} items.")
        return producers

    def initialize_consumers(self) -> List[Consumer]:
        """
        Initializes and returns a list of Consumer objects.

        :return: A list of initialized Consumer objects.
        :rtype: List[Consumer]
        """
        items_per_consumer, leftover_items = self.get_num_items_to_consume()
        consumers: List[Consumer] = []
        for i in range(self.num_consumers):
            items_to_consume: int = items_per_consumer + (1 if i < leftover_items else 0)
            consumers.append(Consumer(i + 1,
                                      self.consumer_speed_range[0],
                                      self.consumer_speed_range[1],
                                      self.buffer,
                                      items_to_consume,
                                      self.statistic_tracker))
            logging.debug(f"Consumer {i + 1} will consume {items_to_consume} items.")
        return consumers

    def get_num_items_to_produce(self) -> Tuple[int, int]:
        """
        Calculates the number of items each producer will handle and the
        remaining items that are unassigned.

        :return: A tuple where the first element is the number of items
        assigned to each producer, and the second element is the leftover
        items that are unassigned after distribution.
        :rtype: Tuple[int, int]
        """
        items_per_producer: int = self.num_items_to_process // self.num_producers
        leftover_items: int = self.num_items_to_process % self.num_producers
        return items_per_producer, leftover_items

    def get_num_items_to_consume(self) -> Tuple[int, int]:
        """
        Calculates the number of items each consumer will handle and the
        remaining items that are unassigned.

        :return: A tuple where the first element is the number of items
        assigned to each consumer, and the second element is the leftover
        items that are unassigned after distribution.
        :rtype: Tuple[int, int]
        """
        items_per_consumer: int = self.num_items_to_process // self.num_consumers
        leftover_items: int = self.num_items_to_process % self.num_consumers
        return items_per_consumer, leftover_items

    def join_all(self) -> None:
        """
        Join all running threads for producers and consumers.

        :return: This method does not return any value.
        :rtype: None
        """
        self.join_producers()
        self.join_consumers()

    def join_producers(self) -> None:
        """
        Join all producer threads running in the system.

        :return: This method does not return any value.
        :rtype: None
        """
        for producer in self.producers:
            producer.join()

    def join_consumers(self) -> None:
        """
        Join all consumer threads running in the system.

        :return: This method does not return any value.
        :rtype: None
        """
        for consumer in self.consumers:
            consumer.join()

    def start_all(self) -> None:
        """
        Starts all producer and consumer threads.

        :return: This method does not return any value.
        :rtype: None
        """
        threads: List[threading.Thread] = self.producers + self.consumers
        random.shuffle(threads)
        logging.debug(f"Number of threads: {len(threads)}.")
        for thread in threads:
            thread.start()
        self.threads_started = True