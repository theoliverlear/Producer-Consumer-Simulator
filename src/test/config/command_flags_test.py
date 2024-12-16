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

    def test_error_handling(self):
        buffer_size_flag = CommandFlags.BUFFER_SIZE.value
        self.assertEqual(buffer_size_flag.flag, "-b")
        self.assertEqual(buffer_size_flag.full_flag, "--buffer-size")
        self.assertEqual(buffer_size_flag.type, int)
        self.assertEqual(buffer_size_flag.default_value, 100)
        self.assertEqual(buffer_size_flag.help_text, "Buffer size in bytes")

        num_items_flag = CommandFlags.NUM_ITEMS.value
        self.assertEqual(num_items_flag.flag, "-n")
        self.assertEqual(num_items_flag.full_flag, "--num-items")
        self.assertEqual(num_items_flag.type, int)
        self.assertEqual(num_items_flag.default_value, 100)
        self.assertEqual(num_items_flag.help_text, "Number of items to process")

        self.assertEqual(str(buffer_size_flag), "CommandFlag(-b, --buffer-size, <class 'int'>, 100, Buffer size in bytes)")


if __name__ == '__main__':
    unittest.main()
