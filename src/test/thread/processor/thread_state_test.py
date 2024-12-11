import unittest

from src.main.thread.processor.thread_state import ThreadState


class MyTestCase(unittest.TestCase):
    def test_instantiation(self):
        self.assertEqual(ThreadState.ACTIVE.value, ('active',))
        self.assertEqual(ThreadState.INACTIVE.value, ('inactive',))


if __name__ == '__main__':
    unittest.main()
