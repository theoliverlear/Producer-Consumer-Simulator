import unittest
from unittest.mock import Mock

from src.main.config.config import Config
from src.main.suggestion.buffer_suggester import BufferSuggester, BufferSuggestions


class BufferSuggesterTest(unittest.TestCase):
    def test_instantiation(self):
        config = Config(10, 100, 2, 2, (1, 3), (2, 4), False, True)
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

    def test_value_change(self):
        config = Mock(buffer_size=10)
        tracker = Mock(num_full_buffer=0, num_empty_buffer=0, num_items_to_process=100)
        suggester = BufferSuggester(config, tracker)

        tracker.num_full_buffer = 15
        tracker.num_empty_buffer = 0
        suggester.calculate()
        self.assertEqual(suggester.suggestion, BufferSuggestions.INCREASE_BUFFER_SIZE)

        tracker.num_full_buffer = 0
        tracker.num_empty_buffer = 20
        suggester.calculate()
        self.assertEqual(suggester.suggestion, BufferSuggestions.DECREASE_BUFFER_SIZE)

    def test_function_io(self):
        config = Mock(buffer_size=10)
        tracker = Mock(num_full_buffer=5, num_empty_buffer=2, num_items_to_process=20)
        suggester = BufferSuggester(config, tracker)

        suggester.calculate()

        self.assertIn(suggester.suggestion, [
            BufferSuggestions.INCREASE_BUFFER_SIZE,
            BufferSuggestions.DECREASE_BUFFER_SIZE,
            BufferSuggestions.KEEP_BUFFER_SIZE
        ])


if __name__ == '__main__':
    unittest.main()
