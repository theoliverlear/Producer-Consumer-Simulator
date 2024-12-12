import unittest
from unittest.mock import Mock, MagicMock

from src.main.buffer.full_buffer_exception import FullBufferException
from src.main.thread.processor.producer.producer import Producer


class ProducerTest(unittest.TestCase):
    def test_instantiation(self):
        producer = Producer(1, 5, 10, Mock(), 100, Mock())

        self.assertEqual(producer.id, 1)
        self.assertEqual(producer.speed_floor, 5)
        self.assertEqual(producer.speed_ceiling, 10)
        self.assertEqual(producer.num_items_to_process, 100)
        self.assertEqual(producer.name, "Producer-1")
        self.assertFalse(producer.running)

    def test_value_change(self):
        buffer = Mock()
        tracker = Mock(num_items_to_process=10, items_produced=5)  # Set valid integers
        producer = Producer(1, 1, 3, buffer, 10, tracker)

        buffer.enqueue.return_value = None
        producer.process_item()
        self.assertEqual(producer.num_items_to_process, 9)

        buffer.enqueue.side_effect = FullBufferException
        producer.process_item()
        self.assertEqual(producer.num_items_to_process, 9)

        tracker.num_items_to_process = 10
        tracker.items_produced = 10
        producer.stop()
        self.assertFalse(producer.running)

    def test_function_io(self):
        buffer = Mock()
        tracker = Mock()
        tracker.num_items_to_process = 5
        tracker.items_produced = 1

        producer = Producer(1, 1, 3, buffer, 5, tracker)

        buffer.enqueue.return_value = None
        producer.process_item()
        buffer.enqueue.assert_called_once()
        self.assertEqual(producer.num_items_to_process, 4)

        producer.stop()
        self.assertFalse(producer.running)

    def test_execution(self):
        mock_buffer = MagicMock()
        mock_stat_tracker = MagicMock()
        mock_stat_tracker.num_items_to_process = 10
        mock_stat_tracker.items_produced = 5

        producer = Producer(
            id=1,
            speed_floor=1,
            speed_ceiling=2,
            buffer=mock_buffer,
            num_items_to_process=5,
            statistic_tracker=mock_stat_tracker
        )

        producer.process_item()
        self.assertEqual(producer.num_items_to_process, 4)
        mock_buffer.enqueue.assert_called_once()


if __name__ == '__main__':
    unittest.main()
