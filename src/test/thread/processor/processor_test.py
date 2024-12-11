import unittest
from unittest.mock import Mock, create_autospec, patch

from src.main.thread.processor.processor import Processor
from src.main.thread.processor.producer.producer import Producer


class ProccessorTest(unittest.TestCase):
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
        tracker = Mock(num_items_to_process=10)
        processor = create_autospec(Processor, instance=True)
        processor.id = 1
        processor.speed_floor = 1
        processor.speed_ceiling = 3
        processor.num_items_to_process = 10
        processor.running = True

        self.assertEqual(processor.num_items_to_process, 10)
        self.assertEqual(processor.speed_floor, 1)
        self.assertEqual(processor.speed_ceiling, 3)

        processor.num_items_to_process -= 1
        self.assertEqual(processor.num_items_to_process, 9)

        processor.running = True
        processor.stop = Mock()
        processor.stop()
        processor.stop.assert_called_once()

    @patch.multiple(Processor, __abstractmethods__=set())
    def test_function_io(self):
        buffer = Mock()
        tracker = Mock()
        processor = Processor(1, 1, 3, buffer, 5, tracker)

        processor.run = Mock()
        processor.stop = Mock()
        processor.process_item = Mock()

        processor.simulate_processing()
        tracker.increment_produced_items.assert_not_called()

        processor.stop()
        processor.stop.assert_called_once()
        self.assertFalse(processor.running)


if __name__ == '__main__':
    unittest.main()
