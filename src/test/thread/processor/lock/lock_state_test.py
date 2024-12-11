import unittest

from src.main.thread.processor.lock.lock_state import LockState


class MyTestCase(unittest.TestCase):
    def test_instantiation(self):
        self.assertEqual(LockState.AVAILABLE.value, ('available',))
        self.assertEqual(LockState.UNAVAILABLE.value, ('unavailable',))


if __name__ == '__main__':
    unittest.main()
