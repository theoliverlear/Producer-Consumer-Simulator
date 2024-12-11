import unittest
from unittest.mock import Mock

from src.main.config.config import Config
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


if __name__ == '__main__':
    unittest.main()
