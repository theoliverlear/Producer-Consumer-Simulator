import argparse
import unittest
from unittest.mock import Mock, patch

from src.main.config.command_flag import CommandFlag
from src.main.config.command_parser import set_parser_args, get_config_from_arguments


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
        parser = argparse.ArgumentParser()
        mock_flag = Mock(
            flag='-b',
            full_flag='--buffer-size',
            type=int,
            default_value=100,
            help_text='Buffer size'
        )

        parser = set_parser_args(parser, mock_flag)
        args = parser.parse_args(['-b', '200'])
        self.assertEqual(args.buffer_size, 200)

        mock_flag.default_value = 300
        parser = argparse.ArgumentParser()  # Reset the parser
        parser = set_parser_args(parser, mock_flag)
        args = parser.parse_args([])
        self.assertEqual(args.buffer_size, 300)

    def test_function_io(self):
        args = ['-b', '128', '-n', '500', '-p', '2', '-c', '3', '-v']
        mock_config = Mock()
        mock_config.buffer_size = 128
        mock_config.num_items = 500
        mock_config.num_producers = 2
        mock_config.num_consumers = 3
        mock_config.verbose = True

        with patch('src.main.config.command_parser.Config', return_value=mock_config):
            config = get_config_from_arguments(args)

        self.assertEqual(config.buffer_size, 128)
        self.assertEqual(config.num_items, 500)
        self.assertEqual(config.num_producers, 2)
        self.assertEqual(config.num_consumers, 3)
        self.assertTrue(config.verbose)

    @patch("src.main.config.command_parser.CommandFlag")
    def test_execution(self, MockCommandFlag):
        mock_flag = MockCommandFlag.return_value
        mock_flag.flag = "-f"
        mock_flag.full_flag = "--full-flag"
        mock_flag.type = str
        mock_flag.default_value = "default"
        mock_flag.help_text = "help text"

        # Mock the parser
        parser = Mock()
        set_parser_args(parser, mock_flag)

        # Simulate parser calls
        parser.add_argument.assert_called_once_with(
            "-f", "--full-flag", type=str, default="default", help="help text"
        )


if __name__ == '__main__':
    unittest.main()
