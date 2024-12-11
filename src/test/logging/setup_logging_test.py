import unittest

from src.main.logging.setup_logging import (setup_logging,
                                            setup_default_logging,
                                            setup_verbose_logging,
                                            execution_trace)


class SetupLoggingTest(unittest.TestCase):
    def test_instantiation(self):
        self.assertTrue(callable(setup_logging))
        self.assertTrue(callable(setup_default_logging))
        self.assertTrue(callable(setup_verbose_logging))
        self.assertTrue(callable(execution_trace))

    def test_execution_trace_decorator(self):
        @execution_trace
        def test_function():
            return "Test"

        result = test_function()
        self.assertEqual(result, "Test")



if __name__ == '__main__':
    unittest.main()
