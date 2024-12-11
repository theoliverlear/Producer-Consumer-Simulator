import unittest
from unittest.mock import Mock

from src.main.config.config import Config
from src.main.suggestion.buffer_suggester import BufferSuggester, BufferSuggestions


class BufferSuggesterTest(unittest.TestCase):
    def test_instantiation(self):
        config = Config(10,
                        100,
                        2,
                        2,
                        (1, 3),
                        (2, 4),
                        False,
                        True)
        statistic_tracker = Mock(num_full_buffer=0,
                                 num_empty_buffer=0,
                                 num_items_to_process=100)
        suggester = BufferSuggester(config,
                                    statistic_tracker)

        self.assertEqual(suggester.config, config)
        self.assertEqual(suggester.statistic_tracker, statistic_tracker)
        self.assertEqual(suggester.buffer_size, 10)
        self.assertEqual(suggester.num_full_buffer, 0)
        self.assertEqual(suggester.num_empty_buffer, 0)
        self.assertEqual(suggester.num_items_to_process, 0)
        self.assertEqual(suggester.suggestion, BufferSuggestions.KEEP_BUFFER_SIZE)


if __name__ == '__main__':
    unittest.main()
