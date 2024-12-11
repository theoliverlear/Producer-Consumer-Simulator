import unittest
from unittest.mock import patch

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
        with patch('src.main.logging.logging_utilities.logging.info') as mock_log:
            log_in_bold("Test Message")
            mock_log.assert_called_with("\033[1mTest Message\033[0m")

            print_logging_seperator()
            mock_log.assert_called_with("\n" + "-" * 60)


if __name__ == '__main__':
    unittest.main()
