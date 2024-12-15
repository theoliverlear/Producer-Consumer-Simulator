import logging
from abc import ABC, abstractmethod

from src.main.statistics.statistic_tracker import StatisticTracker


class Buffer(ABC):
    """
    Abstract base class for a buffer data structure.

    This class serves as a blueprint for creating buffer implementations with
    a fixed size. It provides abstract methods for enqueueing and dequeueing
    operations, as well as checking if the buffer is empty or full. The class
    also interacts with a statistic tracker to monitor buffer-related metrics.

    :ivar buffer_size: The maximum number of elements the buffer can hold.
    :type buffer_size: int
    :ivar statistic_tracker: The statistic tracking object associated
        with the buffer for monitoring buffer operations.
    :type statistic_tracker: StatisticTracker
    """
    def __init__(self,
                 buffer_size: int,
                 statistic_tracker: StatisticTracker):
        """
        Initializes the Buffer class with a specified buffer size and a
        statistic tracker.

        The buffer size determines how much data can be stored at a time. The
        statistic tracker enables the class to track usage statistics for the
        buffer.

        :param buffer_size: An integer specifying the size of the buffer.
        :type buffer_size: int
        :param statistic_tracker: An instance of StatisticTracker responsible
            for tracking the buffer's statistics.
        :type statistic_tracker: StatisticTracker
        """
        self.buffer_size: int = buffer_size
        self.statistic_tracker: StatisticTracker = statistic_tracker
        logging.debug(f"Buffer initialized with size {buffer_size}.")

    @abstractmethod
    def enqueue(self, number_to_enqueue: int) -> None:
        """
        Enqueue the provided number into the queue. This method must be
        implemented by subclasses to define the specific behavior of adding an
         item to the queue.

        :raises NotImplementedError: If the method is not overridden in a
        subclass.
        :param number_to_enqueue: The number to be added to the queue.
        :type number_to_enqueue: int
        :return: This method does not return anything.
        :rtype: None
        """
        pass

    @abstractmethod
    def dequeue(self) -> int:
        """
        Abstract method to dequeue an element from a data structure.

        This method is intended to be implemented by subclasses and ensures
        the removal of an item from the data structure. It returns the
        dequeued element and should be overridden to define specific behavior.

        :raises NotImplementedError: If the method is not overridden in a
        subclass.
        :return: The element dequeued from the data structure.
        :rtype: int
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        An abstract method to check whether the collection is empty.

        This method must be implemented by any subclass to determine if the
        collection contains no elements.

        :raises NotImplementedError: If the method is not overridden in a
        subclass.
        :rtype: bool
        :return: True if the collection is empty, otherwise False.
        """
        pass

    @abstractmethod
    def is_full(self) -> bool:
        """
        Represents an abstract method to determine if a container is full.

        This method is expected to be implemented by subclasses
        to provide specific logic for determining the "full" condition.

        :raises NotImplementedError: If the method is not overridden in a
        subclass.
        :return: A boolean indicating whether the resource or container is
        full.
        :rtype: bool
        """
        pass