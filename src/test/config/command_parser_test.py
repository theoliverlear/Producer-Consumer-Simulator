import argparse
import unittest

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


if __name__ == '__main__':
    unittest.main()
