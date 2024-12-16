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
        self.start_time: float = 0
        self.end_time: float = 0

    def test_value_change(self):
        tracker = StatisticTracker(num_items_to_process=100)

        self.assertEqual(tracker.num_items_to_process, 100)
        self.assertEqual(tracker.items_produced, 0)
        self.assertEqual(tracker.items_consumed, 0)

        tracker.increment_produced_items()
        self.assertEqual(tracker.items_produced, 1)

        tracker.increment_consumed_items()
        self.assertEqual(tracker.items_consumed, 1)

        tracker.increment_empty_buffer()
        self.assertEqual(tracker.num_empty_buffer, 1)

        tracker.increment_full_buffer()
        self.assertEqual(tracker.num_full_buffer, 1)

    def test_function_io(self):
        tracker = StatisticTracker(100)

        tracker.increment_produced_items()
        tracker.increment_consumed_items()
        tracker.increment_empty_buffer()
        tracker.increment_full_buffer()

        self.assertEqual(tracker.items_produced, 1)
        self.assertEqual(tracker.items_consumed, 1)
        self.assertEqual(tracker.num_empty_buffer, 1)
        self.assertEqual(tracker.num_full_buffer, 1)

    def test_execution(self):
        tracker = StatisticTracker(num_items_to_process=100)

        tracker.start_tracking()
        tracker.increment_produced_items()
        tracker.increment_consumed_items()
        tracker.increment_empty_buffer()
        tracker.increment_full_buffer()
        tracker.stop_tracking()

        self.assertEqual(tracker.items_produced, 1)
        self.assertEqual(tracker.items_consumed, 1)
        self.assertEqual(tracker.num_empty_buffer, 1)
        self.assertEqual(tracker.num_full_buffer, 1)
        self.assertIsNotNone(tracker.start_time)
        self.assertIsNotNone(tracker.end_time)

    def test_error_handling(self):
        try:
            statistic_tracker = StatisticTracker(num_items_to_process=10)

            statistic_tracker.increment_produced_items()
            statistic_tracker.increment_consumed_items()
            statistic_tracker.add_producer_throughput(100)
            statistic_tracker.add_consumer_throughput(150)

            statistic_tracker.start()
            statistic_tracker.stop()

        except Exception as e:
            self.fail(f"StatisticTracker raised an unexpected exception: {e}")



if __name__ == '__main__':
    unittest.main()
