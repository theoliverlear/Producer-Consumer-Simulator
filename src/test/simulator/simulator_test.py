import unittest
from unittest.mock import Mock, patch, MagicMock

from src.main.config.config import Config
from src.main.simulator.simulator import Simulator


class SimulatorTest(unittest.TestCase):
    def test_instantiation(self):
        config = Config(10, 100, 2, 2, (1, 3), (2, 4), False, True)
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

    def test_function_io(self):
        config = Mock(
            num_items_to_process=100,
            buffer_size=10,
            num_producers=2,
            num_consumers=3,
            consumer_speed_range=(1, 3),
            producer_speed_range=(2, 4),
            verbose=True,
            suggestions=False
        )

        with patch('src.main.simulator.simulator.ThreadManager') as self.MockThreadManager:
            simulator = Simulator(config)

            simulator.start()
            self.MockThreadManager.return_value.start_all.assert_called_once()

            simulator.stop()
            self.MockThreadManager.return_value.join_all.assert_called_once()

    @patch('src.main.simulator.simulator.Simulator.simulate')
    def test_execution_order(self, mock_simulate):
        mock_simulate.return_value = None
        mock_config = MagicMock()
        mock_config.buffer_size = 10
        mock_config.num_items_to_process = 100
        mock_config.num_producers = 2
        mock_config.num_consumers = 2
        mock_config.consumer_speed_range = (1, 2)
        mock_config.producer_speed_range = (1, 2)
        mock_config.suggestions = False

        simulator = Simulator(config=mock_config)
        simulator.simulate()
        mock_simulate.assert_called_once()

    def test_error_handling(self):
        try:
            config_mock = MagicMock(spec=Config)
            config_mock.num_items_to_process = 10
            config_mock.buffer_size = 5
            config_mock.num_producers = 2
            config_mock.num_consumers = 2
            config_mock.consumer_speed_range = (1, 5)
            config_mock.producer_speed_range = (1, 5)
            config_mock.suggestions = False

            simulator = Simulator(config=config_mock)
            simulator.simulate()
        except Exception as e:
            self.fail(f"Simulator raised an unexpected exception: {e}")


if __name__ == '__main__':
    unittest.main()
