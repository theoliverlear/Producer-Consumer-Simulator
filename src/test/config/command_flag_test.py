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

    def test_value_change(self):
        flag = CommandFlag('-b', '--buffer-size', int, 100, 'Buffer size')

        # Validate initial and changed values
        self.assertEqual(flag.flag, '-b')
        flag.flag = '-n'
        self.assertEqual(flag.flag, '-n')

        self.assertEqual(flag.full_flag, '--buffer-size')
        flag.full_flag = '--num-items'
        self.assertEqual(flag.full_flag, '--num-items')

    def test_function_io(self):
        flag = CommandFlag('-b', '--buffer-size', int, 100, 'Buffer size in bytes')

        # Test input/output attributes
        self.assertEqual(flag.flag, '-b')
        self.assertEqual(flag.full_flag, '--buffer-size')
        self.assertEqual(flag.type, int)
        self.assertEqual(flag.default_value, 100)
        self.assertEqual(flag.help_text, 'Buffer size in bytes')

        # Test string representation
        self.assertEqual(
            str(flag),
            "CommandFlag(-b, --buffer-size, <class 'int'>, 100, Buffer size in bytes)"
        )


if __name__ == '__main__':
    unittest.main()
