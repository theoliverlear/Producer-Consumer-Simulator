import unittest
import time
from unittest.mock import Mock, patch

from src.main.statistics.track_performance import track_performance, track_producer_performance, \
    track_consumer_performance, track_exceptions, milliseconds_to_nanoseconds, nanoseconds_to_milliseconds


class TrackPerformanceTest(unittest.TestCase):
    def test_instantiation(self):
        self.assertTrue(callable(track_performance))
        self.assertTrue(callable(track_producer_performance))
        self.assertTrue(callable(track_consumer_performance))
        self.assertTrue(callable(track_exceptions))

    def test_decorators_apply(self):
        @track_performance
        def sample_function():
            return "Test"

        @track_producer_performance
        def producer_function(self):
            return "Producer"

        self.assertEqual(sample_function(), "Test")
        self.assertEqual(producer_function(Mock(statistic_tracker=Mock())), "Producer")

    @patch("time.perf_counter", side_effect=[1.0, 1.5])
    @patch("logging.info")
    def test_value_change(self, mock_logging_info, mock_perf_counter):
        class TestClass:
            @track_performance
            def test_method(self):
                return "Completed"

        obj = TestClass()

        result = obj.test_method()

        self.assertEqual(result, "Completed")

        mock_logging_info.assert_called_with(
            "Execution time for test_method on thread MainThread: 500 milliseconds."
        )

    @patch('src.main.statistics.track_performance.logging.info')
    def test_function_io(self, mock_logging):
        mock_function = Mock(return_value="Result")
        mock_function.__name__ = "mock_function"

        wrapped_function = track_performance(mock_function)

        result = wrapped_function()

        self.assertEqual(result, "Result")
        mock_logging.assert_called_once()

    def test_execution(self):
        @track_performance
        def dummy_function():
            time.sleep(0.001)  # Simulate a small delay
            return "Executed"

        result = dummy_function()

        self.assertEqual(result, "Executed")

    def test_conversion_methods(self):
        self.assertEqual(milliseconds_to_nanoseconds(1), 1000000)
        self.assertAlmostEqual(nanoseconds_to_milliseconds(1000000), 1.0)

if __name__ == '__main__':
    unittest.main()
