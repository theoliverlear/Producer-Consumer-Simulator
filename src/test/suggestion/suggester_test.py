import unittest
from unittest.mock import Mock

from src.main.config.config import Config
from src.main.suggestion.buffer_suggester import BufferSuggestions
from src.main.suggestion.speed_suggester import SpeedSuggestions
from src.main.suggestion.suggester import Suggester


class SuggesterTest(unittest.TestCase):
    def test_instantiation(self):
        config = Config(10, 100, 2, 2,
                        (1, 3), (2, 4), False, True)
        statistic_tracker = Mock()

        suggester = Suggester(config, statistic_tracker)

        self.assertEqual(suggester.config, config)
        self.assertEqual(suggester.statistic_tracker, statistic_tracker)
        self.assertIsNotNone(suggester.buffer_suggester)
        self.assertIsNotNone(suggester.speed_suggester)
        self.assertEqual(suggester.buffer_suggester.config, config)
        self.assertEqual(suggester.speed_suggester.config, config)

    def test_value_change(self):
        config = Mock(
            buffer_size=10,
            num_producers=1,
            num_consumers=2,
            producer_speed_range=(2, 4),
            consumer_speed_range=(1, 3)
        )
        tracker = Mock()

        buffer_suggester = Mock()
        buffer_suggester.suggestion = BufferSuggestions.INCREASE_BUFFER_SIZE

        speed_suggester = Mock()
        speed_suggester.suggestions = [SpeedSuggestions.INCREASE_PRODUCER_SPEED]

        suggester = Suggester(config, tracker)
        suggester.buffer_suggester = buffer_suggester
        suggester.speed_suggester = speed_suggester

        suggester.show_buffer_suggestions()
        buffer_suggester.calculate.assert_called_once()
        buffer_suggester.show_statistics.assert_called_once()
        buffer_suggester.show_suggestions.assert_called_once()

        suggester.show_speed_suggestions()
        speed_suggester.calculate.assert_called_once()
        speed_suggester.show_statistics.assert_called_once()
        speed_suggester.show_suggestions.assert_called_once()

    def test_function_io(self):
        config = Mock()
        tracker = Mock()
        buffer_suggester = Mock()
        speed_suggester = Mock()

        with unittest.mock.patch('src.main.suggestion.suggester.BufferSuggester', return_value=buffer_suggester), \
                unittest.mock.patch('src.main.suggestion.suggester.SpeedSuggester', return_value=speed_suggester):
            suggester = Suggester(config, tracker)
            suggester.show_suggestions()

        buffer_suggester.calculate.assert_called_once()
        buffer_suggester.show_statistics.assert_called_once()
        buffer_suggester.show_suggestions.assert_called_once()
        speed_suggester.calculate.assert_called_once()
        speed_suggester.show_statistics.assert_called_once()
        speed_suggester.show_suggestions.assert_called_once()


if __name__ == '__main__':
    unittest.main()
