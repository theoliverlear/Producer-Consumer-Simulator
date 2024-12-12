import unittest
from unittest.mock import Mock, patch

from src.main.config.command_flags import CommandFlags

class CommandFlagsTest(unittest.TestCase):
    def test_instantiation(self):
        self.assertEqual(CommandFlags.BUFFER_SIZE.value.flag, "-b")
        self.assertEqual(CommandFlags.NUM_ITEMS.value.full_flag, "--num-items")
        self.assertEqual(CommandFlags.NUM_PRODUCERS.value.type, int)
        self.assertEqual(CommandFlags.VERBOSE.value.default_value, False)
        self.assertEqual(CommandFlags.CONSUMER_WORK_SPEED.value.help_text, "Consumer speed range")

    def test_value_change(self):
        self.assertEqual(CommandFlags.BUFFER_SIZE.value.flag, '-b')

        CommandFlags.BUFFER_SIZE.value.flag = '-n'
        self.assertEqual(CommandFlags.BUFFER_SIZE.value.flag, '-n')

        self.assertEqual(CommandFlags.NUM_ITEMS.value.full_flag, '--num-items')
        CommandFlags.NUM_ITEMS.value.full_flag = '--total-items'
        self.assertEqual(CommandFlags.NUM_ITEMS.value.full_flag, '--total-items')

    def test_function_io(self):
        self.assertEqual(CommandFlags.BUFFER_SIZE.value.flag, '-b')
        self.assertEqual(CommandFlags.NUM_ITEMS.value.full_flag, '--num-items')
        self.assertEqual(CommandFlags.VERBOSE.value.type, bool)
        self.assertEqual(CommandFlags.SUGGESTIONS.value.default_value, False)

    @patch("src.main.config.command_flags.CommandFlag")
    def test_execution(self, MockCommandFlag):
        mock_flag = MockCommandFlag.return_value

        mock_flag.configure_mock(
            __str__=Mock(return_value="Mocked String"),
            __repr__=Mock(return_value="Mocked Repr")
        )

        str_result = str(mock_flag)
        repr_result = repr(mock_flag)

        self.assertEqual(str_result, "Mocked String")
        self.assertEqual(repr_result, "Mocked Repr")
        mock_flag.__str__.assert_called_once()
        mock_flag.__repr__.assert_called_once()


if __name__ == '__main__':
    unittest.main()
