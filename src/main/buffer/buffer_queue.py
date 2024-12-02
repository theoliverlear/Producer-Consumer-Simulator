from collections import deque

from src.main.buffer.buffer import Buffer
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.buffer.full_buffer_exception import FullBufferException


class BufferQueue(Buffer):
    def __init__(self, buffer_size: int):
        super().__init__(buffer_size)
        self.buffer: deque = deque(maxlen=buffer_size)

    def is_empty(self) -> bool:
        return len(self.buffer) == 0

    def is_full(self) -> bool:
        return len(self.buffer) == self.buffer.maxlen

    def enqueue(self, number_to_enqueue: int) -> None:
        if len(self.buffer) < self.buffer.maxlen:
            self.buffer.appendleft(number_to_enqueue)
        else:
            raise FullBufferException()

    def dequeue(self) -> int:
        if len(self.buffer) > 0:
            return self.buffer.pop()
        else:
            raise EmptyBufferException()