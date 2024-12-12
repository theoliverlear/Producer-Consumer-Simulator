import unittest
from unittest.mock import MagicMock, Mock, create_autospec

from src.main.buffer.buffer import Buffer
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.statistics.statistic_tracker import StatisticTracker


class BufferTest(unittest.TestCase):
    def test_instantiation(self):
        class MockBuffer(Buffer):
            def enqueue(self, number_to_enqueue: int): pass
            def dequeue(self) -> int: return 0
            def is_empty(self) -> bool: return True
            def is_full(self) -> bool: return False

        buffer_size = 10
        statistic_tracker = MagicMock(spec=StatisticTracker)
        buffer = MockBuffer(buffer_size,
                            statistic_tracker)

        self.assertEqual(buffer.buffer_size,
                         buffer_size)
        self.assertEqual(buffer.statistic_tracker,
                         statistic_tracker)

    def test_value_change(self):
        statistic_tracker_mock = Mock()
        buffer_size = 5

        buffer = Mock(spec=Buffer)
        buffer.buffer_size = buffer_size
        buffer.statistic_tracker = statistic_tracker_mock

        self.assertEqual(buffer.buffer_size, 5)
        self.assertEqual(buffer.statistic_tracker, statistic_tracker_mock)

        buffer.buffer_size = 10
        buffer.statistic_tracker = None

        self.assertEqual(buffer.buffer_size, 10)
        self.assertIsNone(buffer.statistic_tracker)

    def test_function_io(self):
        buffer = create_autospec(Buffer, instance=True, buffer_size=2)
        buffer.enqueue = Mock()
        buffer.dequeue = Mock(side_effect=[10, 20, EmptyBufferException()])
        buffer.is_full.return_value = True
        buffer.is_empty.return_value = True

        buffer.enqueue(10)
        buffer.enqueue(20)
        self.assertTrue(buffer.is_full())
        self.assertEqual(buffer.dequeue(), 10)
        self.assertEqual(buffer.dequeue(), 20)
        with self.assertRaises(EmptyBufferException):
            buffer.dequeue()
        self.assertTrue(buffer.is_empty())


    def test_execution(self):
        buffer = Mock(spec=Buffer)

        buffer.enqueue(1)
        buffer.is_full()
        buffer.dequeue()
        buffer.is_empty()

        self.assertTrue(buffer.enqueue.called)
        self.assertTrue(buffer.is_full.called)
        self.assertTrue(buffer.dequeue.called)
        self.assertTrue(buffer.is_empty.called)

        buffer.enqueue.assert_called_once_with(1)
        buffer.is_full.assert_called_once()
        buffer.dequeue.assert_called_once()
        buffer.is_empty.assert_called_once()


if __name__ == '__main__':
    unittest.main()
