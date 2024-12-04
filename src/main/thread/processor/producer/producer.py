import logging
import random
import time

from src.main.buffer.buffer import Buffer
from src.main.buffer.full_buffer_exception import FullBufferException
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.statistics.track_performance import track_producer_performance
from src.main.thread.processor.processor import Processor


class Producer(Processor):
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
        self.name = f"Producer-{id}"

    @staticmethod
    def get_random_number() -> int:
        return random.randint(1, 100)


    def run(self) -> None:
        self.running = True
        while self.running and self.num_items_to_process > 0:
            self.process_item()
        self.stop()

    @track_producer_performance
    def process_item(self) -> None:
        try:
            random_number: int = self.get_random_number()
            logging.info(f"Enqueued number: {random_number}")
            self.buffer.enqueue(random_number)
            self.num_items_to_process -= 1
        except FullBufferException:
            time.sleep(0.01)
            return
        self.simulate_processing()

    def stop(self):
        self.running = False