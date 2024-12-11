import unittest
from unittest.mock import Mock

from src.main.thread.thread_manager import ThreadManager


class ThreadManagerTest(unittest.TestCase):
    def test_instantiation(self):
        thread_manager = ThreadManager(
            2, 3, (1, 3), (2, 4),
            Mock(), 100, Mock()
        )

        self.assertEqual(thread_manager.num_producers, 2)
        self.assertEqual(thread_manager.num_consumers, 3)
        self.assertEqual(len(thread_manager.producers), 2)
        self.assertEqual(len(thread_manager.consumers), 3)

    def test_value_change(self):
        buffer = Mock()
        tracker = Mock()
        thread_manager = ThreadManager(
            num_producers=2,
            num_consumers=3,
            consumer_speed_range=(1, 2),
            producer_speed_range=(2, 4),
            buffer=buffer,
            num_items_to_process=10,
            statistic_tracker=tracker,
        )

        # Validate producers and consumers
        self.assertEqual(len(thread_manager.producers), 2)
        self.assertEqual(len(thread_manager.consumers), 3)

        # Test joining threads
        for thread in thread_manager.producers + thread_manager.consumers:
            thread.join = Mock()
        thread_manager.join_all()
        for thread in thread_manager.producers + thread_manager.consumers:
            thread.join.assert_called_once()

        # Test starting threads
        for thread in thread_manager.producers + thread_manager.consumers:
            thread.start = Mock()
        thread_manager.start_all()
        for thread in thread_manager.producers + thread_manager.consumers:
            thread.start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
