import logging
from collections import deque

from src.main.buffer.buffer import Buffer
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.buffer.full_buffer_exception import FullBufferException
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.statistics.track_performance import track_performance, \
    track_exceptions
from src.main.thread.critical_section import critical_section
from src.main.thread.processor.lock.mutex_lock import MutexLock


class BufferQueue(Buffer):
    """
    A class that represents a thread-safe buffer queue.

    The class provides functionalities for managing a fixed-size queue with
    concurrent access control. It supports enqueueing and dequeuing elements
    while ensuring thread safety using a mutex lock. Additionally, it includes
    performance tracking, exception handling, and statistics collection.

    :ivar buffer: A deque used to store the elements in the buffer, with a
    fixed maximum length.
    :type buffer: collections.deque
    :ivar mutex_lock: A lock used to manage concurrent access to the buffer.
    :type mutex_lock: MutexLock
    :ivar statistic_tracker: An object used for tracking statistics related to
     the buffer's operation.
    :type statistic_tracker: StatisticTracker
    """
    def __init__(self,
                 buffer_size: int,
                 mutex_lock: MutexLock,
                 statistic_tracker: StatisticTracker):
        """
        Initializes the class with a buffer size, a mutex lock for
        thread-safety, and a statistic tracker for monitoring.

        :param buffer_size: The maximum number of elements the deque buffer
            can hold.
        :type buffer_size: int
        :param mutex_lock: A lock used to synchronize access to the buffer.
        :type mutex_lock: MutexLock
        :param statistic_tracker: An object responsible for tracking relevant
        statistics.
        :type statistic_tracker: StatisticTracker
        """
        super().__init__(buffer_size, statistic_tracker)
        self.buffer: deque = deque(maxlen=buffer_size)
        self.mutex_lock: MutexLock = mutex_lock

    def is_empty(self) -> bool:
        """
        Determines if the buffer is empty.

        This method checks whether the internal buffer has any elements or
        not.

        :return: Boolean indicating whether the buffer is empty or not.
        :rtype: bool
        """
        return len(self.buffer) == 0

    def is_full(self) -> bool:
        """
        Checks if the buffer is full.

        This method verifies whether the number of elements in the buffer has
        reached its maximum capacity as defined by its maximum length.

        :return: True if the buffer is full, False otherwise.
        :rtype: bool
        """
        return len(self.buffer) == self.buffer.maxlen

    @track_performance
    @critical_section
    @track_exceptions
    def enqueue(self, number_to_enqueue: int) -> None:
        """
        Adds a number to the queue if the buffer is not full. If the buffer is
        full, raises a `FullBufferException`.

        This method ensures thread safety using a critical section decorator
        and tracks function performance and exceptions through the applied
        decorators.

        :param number_to_enqueue: The integer value to add to the queue.
        :type number_to_enqueue: int
        :return: None
        :raises FullBufferException: If the buffer is full and no space is
            available to add the number.
        """
        if not self.is_full():
            self.buffer.appendleft(number_to_enqueue)
        else:
            logging.debug("Buffer is full")
            raise FullBufferException()

    @track_performance
    @critical_section
    @track_exceptions
    def dequeue(self) -> int:
        """
        Dequeues an item from the buffer.

        This method removes and returns the last item in the buffer if it is
        not empty. If the buffer is empty, an exception is raised instead.
        The method is decorated with performance tracking, critical section
        locking, and exception tracking functionality.

        :raises EmptyBufferException: Raised when attempting to dequeue from
        an empty buffer.
        :return: The last item in the buffer.
        :rtype: int
        """
        if not self.is_empty():
            return self.buffer.pop()
        else:
            logging.debug("Buffer is empty")
            raise EmptyBufferException()