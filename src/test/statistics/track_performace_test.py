import unittest
from unittest.mock import Mock

from src.main.statistics.track_performance import track_performance, track_producer_performance, \
    track_consumer_performance, track_exceptions


class TrackPerformanceTest(unittest.TestCase):
    def test_instantiation(self):
        # Ensure all decorators are callable
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

if __name__ == '__main__':
    unittest.main()
