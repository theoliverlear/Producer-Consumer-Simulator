from enum import Enum

from src.main.config.command_flag import CommandFlag


class CommandFlags(Enum):
    BUFFER_SIZE = CommandFlag('-b', '--buffer-size', 'int'),
    NUM_PRODUCERS = CommandFlag('-p', '--num-producers', 'int'),
    NUM_CONSUMERS = CommandFlag('-c', '--num-consumers', 'int'),
    PRODUCER_WORK_SPEED = CommandFlag('-ps', '--producer-speed-range', 'int:int'),
    CONSUMER_WORK_SPEED = CommandFlag('-cs', '--consumer-speed-range', 'int:int'),
    VERBOSE = CommandFlag('-v', '--verbose', ''),
    SUGGESTIONS = CommandFlag('-s', '--suggestions', ''),