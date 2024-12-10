import unittest

from src.main.buffer.buffer_queue import BufferQueue
from src.main.config.config import Config
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.thread.processor.lock.mutex_lock import MutexLock


class BufferQueueTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
    def test_instantiation(self):
        buffer_size: int = 9
        mutex_lock: MutexLock = MutexLock()
        num_items_to_process: int = 1000
        num_producers: int = 4
        num_consumers: int = 7
        consumer_speed_range: tuple[int, int] = (4,7)
        producer_speed_range: tuple[int, int] = (3,6)
        verbose: bool = True
        suggestions: bool = True
        statistic_tracker: StatisticTracker = StatisticTracker(
            num_items_to_process
        )
        config: Config = Config(
            buffer_size,
            num_items_to_process,
            num_producers,
            num_consumers,
            consumer_speed_range,
            producer_speed_range,
            verbose,
            suggestions
        )
        buffer_queue: BufferQueue = BufferQueue()

if __name__ == '__main__':
    unittest.main()
