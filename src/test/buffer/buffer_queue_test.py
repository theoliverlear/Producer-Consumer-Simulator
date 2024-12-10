import unittest

from src.main.buffer.buffer_queue import BufferQueue
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.buffer.full_buffer_exception import FullBufferException
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

    def test_buffer_value_changes(self):
        buffer_size = 10
        num_items_to_process = 1000
        mutex_lock = MutexLock()
        statistic_tracker = StatisticTracker(num_items_to_process)
        buffer_queue = BufferQueue(buffer_size,
                                   mutex_lock,
                                   statistic_tracker)
        buffer_queue.enqueue(1)
        self.assertEqual(len(buffer_queue.buffer), 1)

        buffer_queue.dequeue()
        self.assertEqual(len(buffer_queue.buffer), 0)

    def test_buffer_function_io(self):
        buffer_size = 10
        num_items_to_process = 1000
        mutex_lock = MutexLock()
        statistic_tracker = StatisticTracker(num_items_to_process)
        buffer_queue = BufferQueue(buffer_size,
                                   mutex_lock,
                                   statistic_tracker)

        buffer_queue.enqueue(1)
        output = buffer_queue.dequeue()
        self.assertEqual(output, 1)

    def test_execution_order(self):
        buffer_size = 10
        num_items_to_process = 1000
        mutex_lock = MutexLock()
        statistic_tracker = StatisticTracker(num_items_to_process)
        buffer_queue = BufferQueue(buffer_size,
                                   mutex_lock,
                                   statistic_tracker)

        buffer_queue.enqueue(1)
        buffer_queue.enqueue(2)
        self.assertEqual(buffer_queue.dequeue(), 1)
        self.assertEqual(buffer_queue.dequeue(), 2)

    def test_error_handling(self):
        buffer_size = 0
        num_items_to_process = 1000
        mutex_lock = MutexLock()
        statistic_tracker = StatisticTracker(num_items_to_process)

        buffer_queue = BufferQueue(buffer_size, mutex_lock, statistic_tracker)

        with self.assertRaises(FullBufferException):
            buffer_queue.enqueue(1)

        with self.assertRaises(EmptyBufferException):
            buffer_queue.dequeue()

    def test_logging_full_buffer(self):
        buffer_size = 1
        num_items_to_process = 1000
        mutex_lock = MutexLock()
        statistic_tracker = StatisticTracker(num_items_to_process)
        buffer_queue = BufferQueue(buffer_size,
                                   mutex_lock,
                                   statistic_tracker)
        buffer_queue.enqueue(1)

        with self.assertLogs(level='INFO') as log:
            with self.assertRaises(FullBufferException):
                buffer_queue.enqueue(2)
        self.assertIn("Buffer is full", log.output[0])

    def test_logging_empty_buffer(self):
        buffer_size = 1
        num_items_to_process = 1000
        mutex_lock = MutexLock()
        statistic_tracker = StatisticTracker(num_items_to_process)
        buffer_queue = BufferQueue(buffer_size,
                                   mutex_lock,
                                   statistic_tracker)

        with self.assertLogs(level='INFO') as log:
            with self.assertRaises(EmptyBufferException):
                buffer_queue.dequeue()
        self.assertIn("Buffer is empty", log.output[0])

if __name__ == '__main__':
    unittest.main()

   


