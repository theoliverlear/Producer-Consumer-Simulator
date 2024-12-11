import unittest
from unittest.mock import Mock

from src.main.config.config import Config
from src.main.suggestion.speed_suggester import SpeedSuggester, SpeedSuggestions


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

    def test_value_change(self):
        config = Mock(
            producer_speed_range=(2, 4),
            consumer_speed_range=(1, 3),
            num_producers=1,
            num_consumers=2
        )
        tracker = Mock(
            producer_throughput_list=[14_400, 15_000],
            consumer_throughput_list=[18_000, 19_000]
        )
        buffer_suggester = Mock()

        suggester = SpeedSuggester(config, tracker, buffer_suggester)

        suggester.calculate()

        tracker.producer_throughput_list = [2000, 3000]
        tracker.consumer_throughput_list = [1000, 1500]
        suggester.calculate()
        self.assertNotIn(SpeedSuggestions.INCREASE_PRODUCER_SPEED, suggester.suggestions)
        self.assertNotIn(SpeedSuggestions.INCREASE_CONSUMER_SPEED, suggester.suggestions)

        config.num_producers = 1
        config.num_consumers = 3
        suggester.calculate()

    def test_function_io(self):
        config = Mock(
            producer_speed_range=(2, 4),
            consumer_speed_range=(1, 3),
            num_producer=2,
            num_consumer=2
        )
        tracker = Mock(
            producer_throughput_list=[5000, 6000],
            consumer_throughput_list=[2000, 3000]
        )
        buffer_suggester = Mock()
        suggester = SpeedSuggester(config, tracker, buffer_suggester)

        suggester.calculate()


if __name__ == '__main__':
    unittest.main()
