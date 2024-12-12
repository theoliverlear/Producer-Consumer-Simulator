import unittest
from unittest.mock import patch, call

from src.main.logging.logging_utilities import (log_in_bold,
                                                log_with_modifier,
                                                print_logging_seperator,
                                                get_underline_string)


class LoggingUtilitiesTest(unittest.TestCase):
    def test_instantiation(self):
        self.assertTrue(callable(log_in_bold))
        self.assertTrue(callable(log_with_modifier))
        self.assertTrue(callable(print_logging_seperator))
        self.assertTrue(callable(get_underline_string))

    @patch("logging.info")
    def test_value_change(self, mock_logging_info):
        log_in_bold("Test Bold Message")
        mock_logging_info.assert_called_with("\033[1mTest Bold Message\033[0m")

        log_in_bold("Another Bold Message")
        mock_logging_info.assert_called_with("\033[1mAnother Bold Message\033[0m")

        log_with_modifier("Test Modifier Message", "\033[4m")
        mock_logging_info.assert_called_with("\033[4mTest Modifier Message\033[0m")

        log_with_modifier("Test Modifier Message", "\033[3m")
        mock_logging_info.assert_called_with("\033[3mTest Modifier Message\033[0m")

    def test_function_io(self):
        with patch('src.main.logging.logging_utilities.logging.info') as self.mock_log:
            log_in_bold("Test Message")
            self.mock_log.assert_called_with("\033[1mTest Message\033[0m")

            print_logging_seperator()
            self.mock_log.assert_called_with("\n" + "-" * 60)

    def test_execution(self):
        with patch('src.main.logging.logging_utilities.logging.info') as mock_log:
            log_in_bold("Execution Order Test")
            print_logging_seperator()

            calls = mock_log.call_args_list
            self.assertEqual(len(calls), 2)  # Ensure two calls were made

            self.assertEqual(calls[0], call("\033[1mExecution Order Test\033[0m"))
            self.assertEqual(calls[1], call("\n" + "-" * 60))

    def test_error_handling(self):
        try:
            log_in_bold(None)
        except Exception as e:
            self.fail(f"log_in_bold raised an unexpected exception with None: {e}")

        try:
            print_logging_seperator()
        except Exception as e:
            self.fail(f"print_logging_seperator raised an unexpected exception: {e}")


if __name__ == '__main__':
    unittest.main()
