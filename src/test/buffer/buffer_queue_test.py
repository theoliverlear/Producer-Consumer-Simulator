import unittest

from src.main.buffer.buffer_queue import BufferQueue
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.thread.processor.lock.mutex_lock import MutexLock


class BufferQueueTest(unittest.TestCase):

    def test_instantiation(self):
        buffer_size: int = 9
        mutex_lock: MutexLock = MutexLock()
        num_items_to_process: int = 1000
        statistic_tracker: StatisticTracker = StatisticTracker(num_items_to_process)
        buffer_queue: BufferQueue = BufferQueue(buffer_size,
                                                mutex_lock,
                                                statistic_tracker)
        self.assertIsNotNone(buffer_queue)

if __name__ == '__main__':
    unittest.main()
