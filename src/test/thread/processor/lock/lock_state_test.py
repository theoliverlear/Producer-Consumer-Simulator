import unittest

from src.main.thread.processor.lock.lock_state import LockState


class LockStateTest(unittest.TestCase):
    def test_instantiation(self):
        self.assertEqual(LockState.AVAILABLE.value, ('available',))
        self.assertEqual(LockState.UNAVAILABLE.value, ('unavailable',))

    def test_value_change(self):
        self.assertEqual(LockState.AVAILABLE.value, ('available',))
        self.assertEqual(LockState.UNAVAILABLE.value, ('unavailable',))

        current_state = LockState.AVAILABLE
        self.assertEqual(current_state.value, ('available',))

        current_state = LockState.UNAVAILABLE
        self.assertEqual(current_state.value, ('unavailable',))

    def test_function_io(self):
        self.assertEqual(LockState.AVAILABLE.value, ('available',))
        self.assertEqual(LockState.UNAVAILABLE.value, ('unavailable',))


if __name__ == '__main__':
    unittest.main()
