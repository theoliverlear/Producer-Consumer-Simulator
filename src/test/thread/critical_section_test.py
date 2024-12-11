import unittest
from unittest.mock import MagicMock

from src.main.thread.critical_section import critical_section


class CriticalSectionTest(unittest.TestCase):
    def test_instantiation(self):
        class TestClass:
            def __init__(self):
                self.mutex_lock = MagicMock()
                self.mutex_lock.__enter__.return_value = None
                self.mutex_lock.__exit__.return_value = None

            @critical_section
            def test_function(self):
                return "Inside Critical Section"

        obj = TestClass()
        result = obj.test_function()

        self.assertEqual(result, "Inside Critical Section")

        obj.mutex_lock.__enter__.assert_called_once()
        obj.mutex_lock.__exit__.assert_called_once()


if __name__ == '__main__':
    unittest.main()
