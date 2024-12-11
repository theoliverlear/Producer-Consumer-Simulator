import unittest
from unittest.mock import Mock

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


if __name__ == '__main__':
    unittest.main()
