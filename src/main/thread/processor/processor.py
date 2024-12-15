import random
import threading
import time
from abc import ABC, abstractmethod

from src.main.buffer.buffer import Buffer
from src.main.statistics.statistic_tracker import StatisticTracker


class Processor(ABC, threading.Thread):
    """
    Processor abstract base class that extends `threading.Thread`.

    :ivar id: Identifier of the processor.
    :type id: int
    :ivar speed_floor: Minimum speed of processing in milliseconds.
    :type speed_floor: int
    :ivar speed_ceiling: Maximum speed of processing in milliseconds.
    :type speed_ceiling: int
    :ivar buffer: Shared buffer object for processing.
    :type buffer: Buffer
    :ivar running: Indicates if the processor should be running.
    :type running: bool
    :ivar num_items_to_process: Number of items remaining to process.
    :type num_items_to_process: int
    :ivar statistic_tracker: Object for tracking processing statistics.
    :type statistic_tracker: StatisticTracker
    """
    def __init__(self,
                 id: int,
                 speed_floor: int,
                 speed_ceiling: int,
                 buffer: Buffer,
                 num_items_to_process: int,
                 statistic_tracker: StatisticTracker):
        """
        Represents a worker entity responsible for processing a specific
        number of items at a variable speed range. This class is designed for
        multi-threaded environments and interacts with shared resources such
        as a buffer.

        :param id: Unique identifier for the worker.
        :type id: int
        :param speed_floor: Minimum processing speed.
        :type speed_floor: int
        :param speed_ceiling: Maximum processing speed.
        :type speed_ceiling: int
        :param buffer: Shared buffer for item consumption or production.
        :type buffer: Buffer
        :param num_items_to_process: Total number of items the worker should
        process.
        :type num_items_to_process: int
        :param statistic_tracker: Object for tracking processing statistics.
        :type statistic_tracker: StatisticTracker
        """
        super().__init__()
        self.id: int = id
        self.speed_floor: int = speed_floor
        self.speed_ceiling: int = speed_ceiling
        self.buffer: Buffer = buffer
        self.running: bool = False
        self.num_items_to_process: int = num_items_to_process
        self.statistic_tracker: StatisticTracker = statistic_tracker

    @abstractmethod
    def run(self):
        """
        Represents an abstract method that must be implemented in derived
        classes to define the logic for running a specific process or task.

        :raises NotImplementedError: If called directly and not overridden in
        a subclass.

        :return: The method does not return any value.
        :rtype: None
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Represents an abstract method that must be implemented in derived
        classes to define the logic to stop a specific process or task.

        :raises NotImplementedError: If called directly and not overridden in
        a subclass.

        :return: The method does not return any value.
        :rtype: None
        """
        pass

    @abstractmethod
    def process_item(self):
        """
        An abstract method for processing an item.

        :raises NotImplementedError: If called directly and not overridden in
        a subclass.

        :return: The method does not return any value.
        :rtype: None
        """
        pass

    def should_run(self) -> bool:
        """
        Determines whether the process should run based on the state.

        :return: True if the process should run and False otherwise.
        :rtype: bool
        """
        return self.running and self.num_items_to_process > 0

    def get_random_speed(self):
        """
        Returns a random speed within the defined floor and ceiling values.

        :return: Random integer value representing the speed within the
        specified range.
        :rtype: int
        """
        return random.randint(self.speed_floor, self.speed_ceiling)
    
    def simulate_processing(self):
        """
        Simulates processing by sleeping for a random duration within the
        defined speed range.

        :return: This method does not return any value.
        :rtype: None
        """
        processing_time = self.get_random_speed()
        time.sleep(processing_time / 1000)
