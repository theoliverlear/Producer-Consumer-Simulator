import argparse
from typing import List, Tuple

from src.main.config.command_flag import CommandFlag
from src.main.config.command_flags import CommandFlags
from src.main.config.config import Config

def set_parser_args(parser: argparse.ArgumentParser,
                    command_flag: CommandFlag):
    """
    Sets the arguments of an ArgumentParser object based on the specified
    command flag. The function dynamically configures the parser with the
    appropriate argument type, default value (if provided), and help text,
    based on the settings of the given CommandFlag object.

    :param parser: The argparse.ArgumentParser object to which the argument
    configuration will be added.
    :type parser: argparse.ArgumentParser
    :param command_flag: An object representing the command line argument.
    :type command_flag: CommandFlag
    :return: The updated argparse.ArgumentParser object with the new
    configuration added.
    :rtype: argparse.ArgumentParser
    """
    if command_flag.type == bool:
        parser.add_argument(
            command_flag.flag,
            command_flag.full_flag,
            action='store_true',
            help=command_flag.help_text
        )
    else:
        parser.add_argument(
            command_flag.flag,
            command_flag.full_flag,
            type=command_flag.type,
            default=command_flag.default_value,
            help=command_flag.help_text
        )
    return parser


def get_config_from_arguments(args: List[str]) -> Config:
    """
    Parses command line arguments to configure the simulator settings. The
    function uses argparse to process the passed arguments and maps them into
    a `Config` object with attributes representing the simulation parameters.
    An exception is captured and reported if argument parsing fails.

    :param args: A list of strings representing command line arguments.
        Each string corresponds to an argument input by the user.
    :type args: List[str]
    :return: A Config object containing the simulation parameters derived from
     the provided arguments.
    :rtype: Config
    """
    try:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Producers and Consumers Simulator')
        for command_flag in CommandFlags:
            parser = set_parser_args(parser, command_flag.value)
        parsed_args = parser.parse_args(args)
        buffer_size: int = parsed_args.buffer_size
        num_items: int = parsed_args.num_items
        num_producers: int = parsed_args.num_producers
        num_consumers: int = parsed_args.num_consumers
        producer_speed_range: Tuple[int, int] = parse_speed_range(parsed_args.producer_speed_range)
        consumer_speed_range: Tuple[int, int] = parse_speed_range(parsed_args.consumer_speed_range)
        verbose: bool = parsed_args.verbose
        suggestions: bool = parsed_args.suggestions
        return Config(
            buffer_size,
            num_items,
            num_producers,
            num_consumers,
            producer_speed_range,
            consumer_speed_range,
            verbose,
            suggestions
        )
    except Exception as exception:
        print(f"Error parsing arguments: {exception}")
        exit(1)

def parse_speed_range(speed_string: str) -> Tuple[int, int]:
    """
    Parses a speed range string in the format 'floor:ceiling' and
    returns the corresponding integer values as a tuple.

    :param speed_string: A string representing a speed range in the
        format 'floor:ceiling' where floor and ceiling are integers.
    :type speed_string: str
    :return: A tuple containing two integers, where the first element
        represents the floor value and the second element represents
        the ceiling value of the speed range.
    :rtype: Tuple[int, int]
    """
    floor, ceiling = map(int, speed_string.split(':'))
    return floor, ceiling