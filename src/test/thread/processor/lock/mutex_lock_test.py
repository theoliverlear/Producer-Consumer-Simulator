import threading
import unittest
from unittest.mock import MagicMock, Mock

from src.main.thread.processor.lock.lock_state import LockState
from src.main.thread.processor.lock.mutex_lock import MutexLock


class MutexLockTest(unittest.TestCase):
    def test_instantiation(self):
        mutex_lock = MutexLock()

        self.assertEqual(mutex_lock.lock_state, LockState.AVAILABLE)
        self.assertIsNotNone(mutex_lock.condition)
        self.assertIsInstance(mutex_lock.condition, threading.Condition)

    def test_value_change(self):
        mutex_lock = MutexLock()

        self.assertEqual(mutex_lock.lock_state, LockState.AVAILABLE)
        mutex_lock.lock()
        self.assertEqual(mutex_lock.lock_state, LockState.UNAVAILABLE)
        mutex_lock.unlock()
        self.assertEqual(mutex_lock.lock_state, LockState.AVAILABLE)

        mutex_lock.lock()
        self.assertTrue(mutex_lock.is_locked())
        mutex_lock.unlock()
        self.assertTrue(mutex_lock.is_available())

        mock_condition = MagicMock()
        mutex_lock.condition = mock_condition
        mutex_lock.acquire()
        mock_condition.__enter__.assert_called_once()
        mutex_lock.release()
        mock_condition.notify_all.assert_called_once()

    def test_function_io(self):
        lock = MutexLock()

        lock.lock()
        self.assertTrue(lock.is_locked())

        lock.unlock()
        self.assertTrue(lock.is_available())

        condition_mock = MagicMock()
        lock.condition = condition_mock

        lock.acquire()
        condition_mock.__enter__.assert_called_once()

        lock.release()
        condition_mock.notify_all.assert_called_once()


if __name__ == '__main__':
    unittest.main()
