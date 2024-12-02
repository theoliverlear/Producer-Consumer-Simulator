from collections import deque

from src.main.buffer.buffer import Buffer
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.buffer.full_buffer_exception import FullBufferException
from src.main.thread.processor.lock.mutex_lock import MutexLock


class BufferQueue(Buffer):
    def __init__(self, buffer_size: int, num_items_to_process: int, mutex_lock: MutexLock):
        super().__init__(buffer_size, num_items_to_process)
        self.buffer: deque = deque(maxlen=buffer_size)
        self.mutex_lock = mutex_lock

    def is_empty(self) -> bool:
        return len(self.buffer) == 0

    def is_full(self) -> bool:
        return len(self.buffer) == self.buffer.maxlen

    def enqueue(self, number_to_enqueue: int) -> None:
        with self.mutex_lock.lock:
            if len(self.buffer) < self.buffer.maxlen:
                self.num_items_to_process -= 1
                self.buffer.appendleft(number_to_enqueue)
            else:
                raise FullBufferException()

    def dequeue(self) -> int:
        with self.mutex_lock.lock:
            if len(self.buffer) > 0:
                return self.buffer.pop()
            else:
                raise EmptyBufferException()