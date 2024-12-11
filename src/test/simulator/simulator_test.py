import unittest
from unittest.mock import Mock

from src.main.config.config import Config
from src.main.simulator.simulator import Simulator


class SimulatorTest(unittest.TestCase):
    def test_instantiation(self):
        config = Config(10,
                        100,
                        2,
                        2,
                        (1, 3),
                        (2, 4),
                        False,
                        True)
        simulator = Simulator(config)

        self.assertEqual(simulator.config, config)
        self.assertIsNotNone(simulator.statistic_tracker)
        self.assertIsNotNone(simulator.buffer)
        self.assertIsNotNone(simulator.thread_manager)

    def test_value_change(self):
        config_mock = Mock()
        config_mock.buffer_size = 10
        config_mock.num_items_to_process = 100
        config_mock.num_producers = 2
        config_mock.num_consumers = 2
        config_mock.consumer_speed_range = (1, 3)
        config_mock.producer_speed_range = (2, 4)
        config_mock.suggestions = False

        statistic_tracker_mock = Mock()

        simulator = Simulator(config_mock)

        self.assertEqual(simulator.is_running, False)
        self.assertEqual(simulator.config.buffer_size, 10)

        simulator.is_running = True
        simulator.config.buffer_size = 20

        self.assertTrue(simulator.is_running)
        self.assertEqual(simulator.config.buffer_size, 20)


if __name__ == '__main__':
    unittest.main()
