import logging
import random
import time

from src.main.buffer.buffer import Buffer
from src.main.buffer.full_buffer_exception import FullBufferException
from src.main.thread.processor.processor import Processor


class Producer(Processor):
    def __init__(self, speed_floor: int, speed_ceiling: int, buffer: Buffer, num_items_to_process: int):
        super().__init__(speed_floor, speed_ceiling, buffer, num_items_to_process)


    @staticmethod
    def get_random_number() -> int:
        return random.randint(1, 100)


    def run(self) -> None:
        self.running = True
        while self.running and self.num_items_to_process > 0:
            random_number: int = self.get_random_number()
            try:
                logging.info(f"Enqueued number: {random_number}")
                self.buffer.enqueue(random_number)
                self.num_items_to_process -= 1
            except FullBufferException:
                time.sleep(0.01)
                continue
            self.simulate_processing()
        self.stop()

    def stop(self):
        self.running = False