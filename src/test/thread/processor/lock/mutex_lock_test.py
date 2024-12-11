import threading
import unittest

from src.main.thread.processor.lock.lock_state import LockState
from src.main.thread.processor.lock.mutex_lock import MutexLock


class MutexLockTest(unittest.TestCase):
    def test_instantiation(self):
        mutex_lock = MutexLock()

        self.assertEqual(mutex_lock.lock_state, LockState.AVAILABLE)
        self.assertIsNotNone(mutex_lock.condition)
        self.assertIsInstance(mutex_lock.condition, threading.Condition)


if __name__ == '__main__':
    unittest.main()
