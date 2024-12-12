import unittest
from unittest.mock import Mock

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

        self.assertEqual(flag.flag, '-b')
        flag.flag = '-n'
        self.assertEqual(flag.flag, '-n')

        self.assertEqual(flag.full_flag, '--buffer-size')
        flag.full_flag = '--num-items'
        self.assertEqual(flag.full_flag, '--num-items')

    def test_function_io(self):
        flag = CommandFlag('-b', '--buffer-size', int, 100, 'Buffer size in bytes')

        self.assertEqual(flag.flag, '-b')
        self.assertEqual(flag.full_flag, '--buffer-size')
        self.assertEqual(flag.type, int)
        self.assertEqual(flag.default_value, 100)
        self.assertEqual(flag.help_text, 'Buffer size in bytes')

        self.assertEqual(
            str(flag),
            "CommandFlag(-b, --buffer-size, <class 'int'>, 100, Buffer size in bytes)"
        )

    def test_execution(self):
        flag = Mock(spec=CommandFlag)

        flag.__str__ = Mock(return_value="Mocked String")
        flag.__repr__ = Mock(return_value="Mocked Repr")

        str_result = flag.__str__()
        repr_result = flag.__repr__()

        self.assertEqual(str_result, "Mocked String")
        self.assertEqual(repr_result, "Mocked Repr")
        flag.__str__.assert_called_once()
        flag.__repr__.assert_called_once()


if __name__ == '__main__':
    unittest.main()
