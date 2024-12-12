import unittest

from src.main.thread.processor.thread_state import ThreadState


class MyTestCase(unittest.TestCase):
    def test_instantiation(self):
        self.assertEqual(ThreadState.ACTIVE.value, ('active',))
        self.assertEqual(ThreadState.INACTIVE.value, ('inactive',))

    def test_value_change(self):
        self.assertEqual(ThreadState.ACTIVE.value, ('active',))
        self.assertEqual(ThreadState.INACTIVE.value, ('inactive',))

        current_state = ThreadState.ACTIVE
        self.assertEqual(current_state.value, ('active',))

        current_state = ThreadState.INACTIVE
        self.assertEqual(current_state.value, ('inactive',))

    def test_function_io(self):
        self.assertEqual(ThreadState.ACTIVE.value, ('active',))
        self.assertEqual(ThreadState.INACTIVE.value, ('inactive',))

    def test_execution(self):
        self.assertEqual(ThreadState.ACTIVE.value, ('active',))
        self.assertEqual(ThreadState.INACTIVE.value, ('inactive',))


if __name__ == '__main__':
    unittest.main()
