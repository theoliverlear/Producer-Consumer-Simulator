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
            level=10,
            format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
            datefmt='%H:%M:%S',
        )

    def test_function_io(self):
        with patch('src.main.logging.setup_logging.logging.basicConfig') as self.mock_logging:
            setup_default_logging()
            self.mock_logging.assert_called_once_with(
                level=20,
                format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
                datefmt='%H:%M:%S'
            )

            self.mock_logging.reset_mock()
            setup_verbose_logging()
            self.mock_logging.assert_called_once_with(
                level=10,
                format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
                datefmt='%H:%M:%S'
            )

    def test_execution(self):
        with patch('src.main.logging.setup_logging.setup_verbose_logging') as self.mock_verbose, \
                patch('src.main.logging.setup_logging.setup_default_logging') as self.mock_default:

            setup_logging(use_verbose=True)
            self.mock_verbose.assert_called_once()
            self.mock_default.assert_not_called()

            setup_logging(use_verbose=False)
            self.mock_default.assert_called_once()
            self.mock_verbose.assert_called_once()  # Ensures only one verbose call


if __name__ == '__main__':
    unittest.main()
