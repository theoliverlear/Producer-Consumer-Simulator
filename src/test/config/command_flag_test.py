import unittest

from src.main.config.command_flag import CommandFlag


class CommandFlagTest(unittest.TestCase):
    def test_instantiation(self):
        command_flag = CommandFlag("-b", "--buffer-size", int, 10, "Specifies the size of the buffer.")

        self.assertEqual(command_flag.flag, "-b")
        self.assertEqual(command_flag.full_flag, "--buffer-size")
        self.assertEqual(command_flag.type, int)
        self.assertEqual(command_flag.default_value, 10)
        self.assertEqual(command_flag.help_text, "Specifies the size of the buffer.")
        self.assertEqual(str(command_flag), "CommandFlag(-b, --buffer-size, <class 'int'>, 10, Specifies the size of the buffer.)")



if __name__ == '__main__':
    unittest.main()
