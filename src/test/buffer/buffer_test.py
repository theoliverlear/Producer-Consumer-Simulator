import unittest
from unittest.mock import MagicMock, Mock

from src.main.buffer.buffer import Buffer
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


if __name__ == '__main__':
    unittest.main()
