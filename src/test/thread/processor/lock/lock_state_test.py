import unittest

from src.main.thread.processor.lock.lock_state import LockState


class LockStateTest(unittest.TestCase):
    def test_instantiation(self):
        self.assertEqual(LockState.AVAILABLE.value, ('available',))
        self.assertEqual(LockState.UNAVAILABLE.value, ('unavailable',))

    def test_value_change(self):
        # Validate initial state
        self.assertEqual(LockState.AVAILABLE.value, ('available',))
        self.assertEqual(LockState.UNAVAILABLE.value, ('unavailable',))

        # Change value and validate
        current_state = LockState.AVAILABLE
        self.assertEqual(current_state.value, ('available',))

        # Transition to UNAVAILABLE
        current_state = LockState.UNAVAILABLE
        self.assertEqual(current_state.value, ('unavailable',))


if __name__ == '__main__':
    unittest.main()
