import unittest
from unittest.mock import Mock

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


if __name__ == '__main__':
    unittest.main()
