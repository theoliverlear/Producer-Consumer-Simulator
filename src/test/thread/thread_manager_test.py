import unittest
from unittest.mock import Mock

from src.main.thread.thread_manager import ThreadManager


class ThreadManagerTest(unittest.TestCase):
    def test_instantiation(self):
        thread_manager = ThreadManager(
            2, 3, (1, 3), (2, 4),
            Mock(), 100, Mock()
        )

        self.assertEqual(thread_manager.num_producers, 2)
        self.assertEqual(thread_manager.num_consumers, 3)
        self.assertEqual(len(thread_manager.producers), 2)
        self.assertEqual(len(thread_manager.consumers), 3)


if __name__ == '__main__':
    unittest.main()
