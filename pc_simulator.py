import sys

from src.main.config.command_parser import get_config_from_arguments
from src.main.config.config import Config
from src.main.logging.setup_logging import setup_logging
from src.main.simulator.simulator import Simulator


def main():
    config: Config = get_config_from_arguments(sys.argv[1:])
    setup_logging(config.verbose)
    simulator: Simulator = Simulator(config)
    simulator.simulate()


if __name__ == "__main__":
    main()