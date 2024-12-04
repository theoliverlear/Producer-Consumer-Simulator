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
    def __init__(self,
                 buffer_size: int,
                 mutex_lock: MutexLock,
                 statistic_tracker: StatisticTracker):
        super().__init__(buffer_size, statistic_tracker)
        self.buffer: deque = deque(maxlen=buffer_size)
        self.mutex_lock = mutex_lock


    def is_empty(self) -> bool:
        return len(self.buffer) == 0

    def is_full(self) -> bool:
        return len(self.buffer) == self.buffer.maxlen

    @track_performance
    @critical_section
    @track_exceptions
    def enqueue(self, number_to_enqueue: int) -> None:
        if len(self.buffer) < self.buffer.maxlen:
            self.buffer.appendleft(number_to_enqueue)
        else:
            logging.info("Buffer is full")
            raise FullBufferException()

    @track_performance
    @critical_section
    @track_exceptions
    def dequeue(self) -> int:
        if len(self.buffer) > 0:
            return self.buffer.pop()
        else:
            logging.info("Buffer is empty")
            raise EmptyBufferException()