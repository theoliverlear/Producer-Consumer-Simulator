import unittest
from unittest.mock import Mock, MagicMock

from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.thread.processor.consumer.consumer import Consumer


class ConsumerTest(unittest.TestCase):
    def test_instantiation(self):
        consumer = Consumer(1, 5, 10, Mock(), 100, Mock())

        self.assertEqual(consumer.id, 1)
        self.assertEqual(consumer.speed_floor, 5)
        self.assertEqual(consumer.speed_ceiling, 10)
        self.assertEqual(consumer.num_items_to_process, 100)
        self.assertEqual(consumer.name, "Consumer-1")
        self.assertFalse(consumer.running)

    def test_value_change(self):
        buffer = Mock()
        tracker = Mock(num_items_to_process=10, items_produced=5)
        consumer = Consumer(1, 1, 3, buffer, 10, tracker)

        buffer.dequeue.return_value = 42
        consumer.process_item()
        self.assertEqual(consumer.num_items_to_process, 9)

        buffer.dequeue.side_effect = EmptyBufferException
        tracker.items_produced = 10
        consumer.process_item()
        self.assertEqual(consumer.num_items_to_process, 9)  # No change

        consumer.stop()
        self.assertFalse(consumer.running)

    def test_function_io(self):
        buffer = Mock()
        tracker = Mock(num_items_to_process=5)
        consumer = Consumer(1, 1, 3, buffer, 5, tracker)

        consumer.process_item()
        buffer.dequeue.assert_called_once()

        consumer.stop()
        self.assertFalse(consumer.running)

    def test_execution(self):
        mock_buffer = MagicMock()
        mock_buffer.dequeue.return_value = 42

        mock_stat_tracker = MagicMock()
        mock_stat_tracker.num_items_to_process = 10
        mock_stat_tracker.items_produced = 10

        consumer = Consumer(
            id=1,
            speed_floor=1,
            speed_ceiling=2,
            buffer=mock_buffer,
            num_items_to_process=5,
            statistic_tracker=mock_stat_tracker
        )

        consumer.process_item()
        self.assertEqual(consumer.num_items_to_process, 4)


if __name__ == '__main__':
    unittest.main()
