import unittest
from unittest.mock import Mock

from src.main.config.config import Config
from src.main.suggestion.speed_suggester import SpeedSuggester


class SpeedSuggesterTest(unittest.TestCase):
    def test_instantiation(self):
        config = Config(10, 100, 2, 2,
                        (1, 3), (2, 4), False, True)
        statistic_tracker = Mock(producer_throughput_list=[], consumer_throughput_list=[])
        buffer_suggester = Mock(suggestion=None)

        suggester = SpeedSuggester(config, statistic_tracker, buffer_suggester)

        self.assertEqual(suggester.config, config)
        self.assertEqual(suggester.statistic_tracker, statistic_tracker)
        self.assertEqual(suggester.buffer_suggester, buffer_suggester)
        self.assertEqual(suggester.intended_producer_speed, 3.0)
        self.assertEqual(suggester.intended_consumer_speed, 2.0)
        self.assertEqual(suggester.suggestions, [])


if __name__ == '__main__':
    unittest.main()
