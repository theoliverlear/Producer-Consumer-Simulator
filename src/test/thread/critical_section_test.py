import unittest
from unittest.mock import MagicMock, Mock

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

    def test_value_change(self):
        test_obj = Mock()
        test_obj.mutex_lock = Mock()

        @critical_section
        def test_method(self):
            return "inside critical section"

        test_obj.test_method = test_method.__get__(test_obj)
        test_obj.mutex_lock.__enter__ = Mock()
        test_obj.mutex_lock.__exit__ = Mock()

        result = test_obj.test_method()
        test_obj.mutex_lock.__enter__.assert_called_once()
        test_obj.mutex_lock.__exit__.assert_called_once()
        self.assertEqual(result, "inside critical section")


if __name__ == '__main__':
    unittest.main()
