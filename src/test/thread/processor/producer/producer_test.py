import unittest
from unittest.mock import Mock

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

        # Test producing an item
        buffer.enqueue.return_value = None
        producer.process_item()
        self.assertEqual(producer.num_items_to_process, 9)

        # Test full buffer exception
        buffer.enqueue.side_effect = FullBufferException
        producer.process_item()
        self.assertEqual(producer.num_items_to_process, 9)

        # Test stop
        tracker.num_items_to_process = 10
        tracker.items_produced = 10
        producer.stop()
        self.assertFalse(producer.running)


if __name__ == '__main__':
    unittest.main()
