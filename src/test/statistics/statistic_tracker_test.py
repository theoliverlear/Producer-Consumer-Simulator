import unittest

from src.main.statistics.statistic_tracker import StatisticTracker


class StatisticTrackerTest(unittest.TestCase):
    def test_instantiation(self):
        tracker = StatisticTracker(num_items_to_process=100)

        self.assertEqual(tracker.num_items_to_process, 100)
        self.assertEqual(tracker.items_produced, 0)
        self.assertEqual(tracker.items_consumed, 0)
        self.assertEqual(tracker.num_empty_buffer, 0)
        self.assertEqual(tracker.num_full_buffer, 0)
        self.assertEqual(tracker.producer_throughput_list, [])
        self.assertEqual(tracker.consumer_throughput_list, [])
        self.assertIsNone(tracker.start_time)
        self.assertIsNone(tracker.end_time)

    def test_value_change(self):
        tracker = StatisticTracker(num_items_to_process=100)

        # Validate initial values
        self.assertEqual(tracker.num_items_to_process, 100)
        self.assertEqual(tracker.items_produced, 0)
        self.assertEqual(tracker.items_consumed, 0)

        # Change values
        tracker.increment_produced_items()
        self.assertEqual(tracker.items_produced, 1)

        tracker.increment_consumed_items()
        self.assertEqual(tracker.items_consumed, 1)

        tracker.increment_empty_buffer()
        self.assertEqual(tracker.num_empty_buffer, 1)

        tracker.increment_full_buffer()
        self.assertEqual(tracker.num_full_buffer, 1)


if __name__ == '__main__':
    unittest.main()
