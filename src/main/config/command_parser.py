import argparse

from src.main.config.command_flag import CommandFlag
from src.main.config.command_flags import CommandFlags
from src.main.config.config import Config

def set_parser_args(parser, command_flag: CommandFlag):
    if command_flag.type == bool:
        parser.add_argument(command_flag.flag, command_flag.full_flag, action='store_true', help=command_flag.help_text)
    else:
        parser.add_argument(command_flag.flag, command_flag.full_flag, type=command_flag.type, default=command_flag.default_value, help=command_flag.help_text)
    return parser


def get_config_from_arguments(args) -> Config:
    parser = argparse.ArgumentParser(description='Producers and Consumers Simulator')
    for command_flag in CommandFlags:
        parser = set_parser_args(parser, command_flag.value)
    parsed_args = parser.parse_args(args)
    buffer_size: int = parsed_args.buffer_size
    num_items: int = parsed_args.num_items
    num_producers: int = parsed_args.num_producers
    num_consumers: int = parsed_args.num_consumers
    producer_speed_range: tuple[int, int] = parse_speed_range(parsed_args.producer_speed_range)
    consumer_speed_range: tuple[int, int] = parse_speed_range(parsed_args.consumer_speed_range)
    verbose: bool = parsed_args.verbose
    suggestions: bool = parsed_args.suggestions
    return Config(buffer_size, num_items, num_producers, num_consumers, producer_speed_range, consumer_speed_range, verbose, suggestions)


def parse_speed_range(speed_string: str) -> tuple[int, int]:
    floor, ceiling = map(int, speed_string.split(':'))
    return floor, ceiling