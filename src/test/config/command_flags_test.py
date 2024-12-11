import unittest
from src.main.config.command_flags import CommandFlags

class CommandFlagsTest(unittest.TestCase):
    def test_instantiation(self):
        self.assertEqual(CommandFlags.BUFFER_SIZE.value.flag, "-b")
        self.assertEqual(CommandFlags.NUM_ITEMS.value.full_flag, "--num-items")
        self.assertEqual(CommandFlags.NUM_PRODUCERS.value.type, int)
        self.assertEqual(CommandFlags.VERBOSE.value.default_value, False)
        self.assertEqual(CommandFlags.CONSUMER_WORK_SPEED.value.help_text, "Consumer speed range")


if __name__ == '__main__':
    unittest.main()
