import unittest
from unittest.mock import Mock

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


if __name__ == '__main__':
    unittest.main()
