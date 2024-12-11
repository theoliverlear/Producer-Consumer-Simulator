import unittest

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



if __name__ == '__main__':
    unittest.main()
