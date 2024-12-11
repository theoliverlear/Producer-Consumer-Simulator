import unittest
from unittest.mock import MagicMock

from src.main.buffer.buffer import Buffer
from src.main.statistics.statistic_tracker import StatisticTracker


class BufferTest(unittest.TestCase):
    def test_buffer_instantiation(self):
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


if __name__ == '__main__':
    unittest.main()
