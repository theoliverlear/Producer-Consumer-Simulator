from enum import Enum
from src.main.config.command_flag import CommandFlag


class CommandFlags(Enum):
    BUFFER_SIZE = CommandFlag('-b', '--buffer-size', int, 100, 'Buffer size in bytes')
    NUM_ITEMS = CommandFlag('-n', '--num-items', int, 1000,'Number of items to process')
    NUM_PRODUCERS = CommandFlag('-p', '--num-producers', int, 1,'Number of producers')
    NUM_CONSUMERS = CommandFlag('-c', '--num-consumers', int, 1,'Number of consumers')
    PRODUCER_WORK_SPEED = CommandFlag('-ps', '--producer-speed-range', str, '1:5','Producer speed range')
    CONSUMER_WORK_SPEED = CommandFlag('-cs', '--consumer-speed-range',str, '1:5','Consumer speed range')
    VERBOSE = CommandFlag('-v', '--verbose', bool, False,'Enable verbose mode')
    SUGGESTIONS = CommandFlag('-s', '--suggestions', bool, False, 'Show suggestions')