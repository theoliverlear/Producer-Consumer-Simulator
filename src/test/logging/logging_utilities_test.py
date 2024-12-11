import unittest

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


if __name__ == '__main__':
    unittest.main()
