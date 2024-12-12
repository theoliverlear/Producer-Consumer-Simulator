import logging
import time
from abc import ABC

from src.main.buffer.buffer import Buffer
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.statistics.track_performance import track_consumer_performance
from src.main.thread.processor.processor import Processor


class Consumer(Processor, ABC):
    def __init__(self,
                 id: int,
                 speed_floor: int,
                 speed_ceiling: int,
                 buffer: Buffer,
                 num_items_to_process: int,
                 statistic_tracker: StatisticTracker):
        super().__init__(id,
                         speed_floor,
                         speed_ceiling,
                         buffer,
                         num_items_to_process,
                         statistic_tracker)
        self.name = f"Consumer-{id}"

    def run(self) -> None:
        self.running = True
        while self.running and self.num_items_to_process > 0:
            self.process_item()
        self.stop()

    @track_consumer_performance
    def process_item(self) -> None:
        try:
            dequeued_number: int = self.buffer.dequeue()
            logging.debug(f"Dequeued number: {dequeued_number}")
            self.num_items_to_process -= 1
            logging.debug(f"Items remaining: {self.num_items_to_process}")
            self.simulate_processing()
        except EmptyBufferException:
            num_remaining_items: int = (self.statistic_tracker.num_items_to_process
                                        - self.statistic_tracker.items_produced)
            num_remaining_string: str = f"{num_remaining_items}"
            logging.debug(f"Buffer is empty. {num_remaining_string} items remaining.")
            has_completed_processing: bool = (self.statistic_tracker.items_produced ==
                                              self.statistic_tracker.num_items_to_process)
            if has_completed_processing:
                self.stop()
            else:
                time.sleep(0.01)
            return

    def stop(self):
        self.running = False