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
        # Validate initial value of a specific flag
        self.assertEqual(CommandFlags.BUFFER_SIZE.value.flag, '-b')

        # Change the flag dynamically and validate
        CommandFlags.BUFFER_SIZE.value.flag = '-n'
        self.assertEqual(CommandFlags.BUFFER_SIZE.value.flag, '-n')

        # Validate initial full_flag and change its value
        self.assertEqual(CommandFlags.NUM_ITEMS.value.full_flag, '--num-items')
        CommandFlags.NUM_ITEMS.value.full_flag = '--total-items'
        self.assertEqual(CommandFlags.NUM_ITEMS.value.full_flag, '--total-items')


if __name__ == '__main__':
    unittest.main()
