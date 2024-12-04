import logging
from abc import ABC, abstractmethod

class Buffer(ABC):
    def __init__(self, buffer_size: int):
        self.buffer_size: int = buffer_size
        self.is_empty: bool = True
        self.is_full: bool = False
        logging.info(f"Buffer initialized with size {buffer_size}")

    @abstractmethod
    def enqueue(self, number_to_enqueue: int) -> None:
        pass

    @abstractmethod
    def dequeue(self) -> int:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def is_full(self) -> bool:
        pass