import unittest

from src.main.config.config import Config


class MyTestCase(unittest.TestCase):
    def test_instantiation(self):
        config = Config(100,
                        1000,
                        2,
                        3,
                        (2, 6),
                        (1, 5),
                        True,
                        False)

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



if __name__ == '__main__':
    unittest.main()
