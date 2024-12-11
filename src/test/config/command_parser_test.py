import argparse
import unittest
from unittest.mock import Mock

from src.main.config.command_flag import CommandFlag
from src.main.config.command_parser import set_parser_args


class CommandParserTest(unittest.TestCase):
    def test_instantiation(self):
        parser = argparse.ArgumentParser()

        int_flag = CommandFlag('-b', '--buffer-size', int, 100, 'Buffer size')
        parser = set_parser_args(parser, int_flag)
        self.assertEqual(parser.parse_args(['-b', '256']).buffer_size, 256)

        bool_flag = CommandFlag('-v', '--verbose', bool, False, 'Verbose mode')
        parser = set_parser_args(parser, bool_flag)
        self.assertTrue(parser.parse_args(['-v']).verbose)
        self.assertFalse(parser.parse_args([]).verbose)

    def test_value_change(self):
        # Create a parser and a mock CommandFlag
        parser = argparse.ArgumentParser()
        mock_flag = Mock(
            flag='-b',
            full_flag='--buffer-size',
            type=int,
            default_value=100,
            help_text='Buffer size'
        )

        # Set the initial argument
        parser = set_parser_args(parser, mock_flag)
        args = parser.parse_args(['-b', '200'])
        self.assertEqual(args.buffer_size, 200)

        # Modify the mock flag's default value and test again
        mock_flag.default_value = 300
        parser = argparse.ArgumentParser()  # Reset the parser
        parser = set_parser_args(parser, mock_flag)
        args = parser.parse_args([])
        self.assertEqual(args.buffer_size, 300)


if __name__ == '__main__':
    unittest.main()
