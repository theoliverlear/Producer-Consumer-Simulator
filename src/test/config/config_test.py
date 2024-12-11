import unittest
from unittest.mock import patch

from src.main.config.config import Config
from src.main.logging.logging_utilities import log_in_bold


class ConfigTest(unittest.TestCase):
    def test_instantiation(self):
        config = Config(100, 1000, 2, 3, (2, 6), (1, 5), True, False)

        self.assertEqual((config.buffer_size,
                          config.num_items_to_process,
                          config.num_producers,
                          config.num_consumers),
                         (100, 1000, 2, 3))
        self.assertEqual((config.consumer_speed_range,
                          config.producer_speed_range,
                          config.verbose,
                          config.suggestions),
                         ((2, 6), (1, 5), True, False))
        self.assertIn("Config(buffer_size=100", str(config))

    def test_value_change(self):
        config = Config(10, 100, 2, 3, (1, 3), (2, 4), False, True)

        self.assertEqual(config.buffer_size, 10)
        self.assertEqual(config.num_items_to_process, 100)
        self.assertEqual(config.num_producers, 2)
        self.assertEqual(config.verbose, False)

        config.buffer_size = 20
        self.assertEqual(config.buffer_size, 20)

        config.verbose = True
        self.assertTrue(config.verbose)

    def test_function_io(self):
        config = Config(
            buffer_size=128,
            num_items_to_process=500,
            num_producers=2,
            num_consumers=3,
            consumer_speed_range=(1, 3),
            producer_speed_range=(2, 4),
            verbose=True,
            suggestions=False
        )

        self.assertEqual(config.buffer_size, 128)
        self.assertEqual(config.num_items_to_process, 500)
        self.assertEqual(config.num_producers, 2)
        self.assertEqual(config.num_consumers, 3)
        self.assertEqual(config.consumer_speed_range, (1, 3))
        self.assertEqual(config.producer_speed_range, (2, 4))
        self.assertTrue(config.verbose)
        self.assertFalse(config.suggestions)


if __name__ == '__main__':
    unittest.main()
