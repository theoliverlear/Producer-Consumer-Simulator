import unittest
from unittest.mock import patch

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

    @patch("logging.basicConfig")
    def test_value_change(self, mock_basic_config):
        setup_logging(False)
        mock_basic_config.assert_called_once()

        setup_logging(True)
        mock_basic_config.assert_called_with(
            level=10,  # DEBUG level
            format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
            datefmt='%H:%M:%S',
        )




if __name__ == '__main__':
    unittest.main()
