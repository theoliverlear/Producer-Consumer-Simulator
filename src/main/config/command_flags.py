from enum import Enum
from src.main.config.command_flag import CommandFlag


class CommandFlags(Enum):
    """
    Represents a collection of command flags used for configuring
    application behavior.

    Each flag contains its corresponding command-line option, short and long
    flags, type, default value, and a description identifying its purpose.

    :ivar BUFFER_SIZE: Command flag for setting the buffer size in items.
    :type BUFFER_SIZE: CommandFlag
    :ivar NUM_ITEMS: Command flag for specifying the number of items to
        process.
    :type NUM_ITEMS: CommandFlag
    :ivar NUM_PRODUCERS: Command flag for setting the number of producers.
    :type NUM_PRODUCERS: CommandFlag
    :ivar NUM_CONSUMERS: Command flag for setting the number of consumers.
    :type NUM_CONSUMERS: CommandFlag
    :ivar PRODUCER_WORK_SPEED: Command flag for configuring the producer
        speed range.
    :type PRODUCER_WORK_SPEED: CommandFlag
    :ivar CONSUMER_WORK_SPEED: Command flag for configuring the consumer
        speed range.
    :type CONSUMER_WORK_SPEED: CommandFlag
    :ivar VERBOSE: Command flag for enabling verbose mode.
    :type VERBOSE: CommandFlag
    :ivar SUGGESTIONS: Command flag for enabling suggestion mode.
    :type SUGGESTIONS: CommandFlag
    """
    BUFFER_SIZE: CommandFlag = CommandFlag('-b', '--buffer-size', int, 100, 'Buffer size in bytes')
    NUM_ITEMS: CommandFlag = CommandFlag('-n', '--num-items', int, 100,'Number of items to process')
    NUM_PRODUCERS: CommandFlag = CommandFlag('-p', '--num-producers', int, 1,'Number of producers')
    NUM_CONSUMERS: CommandFlag = CommandFlag('-c', '--num-consumers', int, 1,'Number of consumers')
    PRODUCER_WORK_SPEED: CommandFlag = CommandFlag('-ps', '--producer-speed-range', str, '1:5','Producer speed range')
    CONSUMER_WORK_SPEED: CommandFlag = CommandFlag('-cs', '--consumer-speed-range',str, '1:5','Consumer speed range')
    VERBOSE: CommandFlag = CommandFlag('-v', '--verbose', bool, False,'Enable verbose mode')
    SUGGESTIONS: CommandFlag = CommandFlag('-s', '--suggestions', bool, False, 'Show suggestions')