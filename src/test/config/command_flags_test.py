import unittest
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


if __name__ == '__main__':
    unittest.main()
