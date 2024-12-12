import unittest
from unittest.mock import Mock, MagicMock, patch

from src.main.config.config import Config
from src.main.suggestion.buffer_suggester import BufferSuggestions
from src.main.suggestion.speed_suggester import SpeedSuggestions, SpeedSuggester
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

    def test_execution(self):
        mock_config = MagicMock()
        mock_config.buffer_size = 10
        mock_config.num_producers = 2
        mock_config.num_consumers = 2

        mock_stat_tracker = MagicMock()
        mock_stat_tracker.num_full_buffer = 5
        mock_stat_tracker.num_empty_buffer = 3
        mock_stat_tracker.num_items_to_process = 50

        mock_stat_tracker.producer_throughput_list = [1000000, 2000000, 1500000]
        mock_stat_tracker.consumer_throughput_list = [1200000, 1300000, 1400000]

        suggester = Suggester(config=mock_config, statistic_tracker=mock_stat_tracker)
        suggester.show_suggestions()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
