import logging
from abc import ABC, abstractmethod

from src.main.statistics.statistic_tracker import StatisticTracker


class Buffer(ABC):
    def __init__(self,
                 buffer_size: int,
                 statistic_tracker: StatisticTracker):
        self.buffer_size: int = buffer_size
        self.statistic_tracker: StatisticTracker = statistic_tracker
        logging.debug(f"Buffer initialized with size {buffer_size}.")

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