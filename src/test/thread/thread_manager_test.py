import unittest
from unittest.mock import Mock, MagicMock

from src.main.thread.thread_manager import ThreadManager


class ThreadManagerTest(unittest.TestCase):
    def test_instantiation(self):
        thread_manager = ThreadManager(
            2, 3, (1, 3), (2, 4), Mock(), 100, Mock()
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

        self.assertEqual(len(thread_manager.producers), 2)
        self.assertEqual(len(thread_manager.consumers), 3)

        for thread in thread_manager.producers + thread_manager.consumers:
            thread.join = Mock()
        thread_manager.join_all()
        for thread in thread_manager.producers + thread_manager.consumers:
            thread.join.assert_called_once()

        for thread in thread_manager.producers + thread_manager.consumers:
            thread.start = Mock()
        thread_manager.start_all()
        for thread in thread_manager.producers + thread_manager.consumers:
            thread.start.assert_called_once()

    def test_function_io(self):
        buffer = Mock()
        tracker = Mock()
        manager = ThreadManager(2, 2, (1, 3), (1, 3), buffer, 10, tracker)

        manager.producers = [Mock()]
        manager.consumers = [Mock()]

        manager.start_all()
        for producer in manager.producers:
            producer.start.assert_called_once()
        for consumer in manager.consumers:
            consumer.start.assert_called_once()

        manager.join_all()
        for producer in manager.producers:
            producer.join.assert_called_once()
        for consumer in manager.consumers:
            consumer.join.assert_called_once()

    def test_execution(self):
        mock_buffer = MagicMock()
        mock_stat_tracker = MagicMock()

        manager = ThreadManager(
            num_producers=2,
            num_consumers=2,
            consumer_speed_range=(1, 2),
            producer_speed_range=(1, 2),
            buffer=mock_buffer,
            num_items_to_process=10,
            statistic_tracker=mock_stat_tracker
        )

        self.assertEqual(len(manager.producers), 2)
        self.assertEqual(len(manager.consumers), 2)

        manager.start_all()
        self.assertTrue(manager.threads_started)


if __name__ == '__main__':
    unittest.main()
