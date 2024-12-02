import logging
import time
from abc import ABC

from src.main.buffer.buffer import Buffer
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.thread.processor.processor import Processor


class Consumer(Processor, ABC):
    def __init__(self, speed_floor: int, speed_ceiling: int, buffer: Buffer, num_items_to_process: int):
        super().__init__(speed_floor, speed_ceiling, buffer, num_items_to_process)
        self.total_items_consumed = 0

    def run(self) -> None:
        self.running = True
        while self.running and self.num_items_to_process > 0:
            try:
                dequeued_number: int = self.buffer.dequeue()
                logging.info(f"Dequeued number: {dequeued_number}")
                self.num_items_to_process -= 1
            except EmptyBufferException:
                time.sleep(0.01)
                continue
            self.simulate_processing()
        self.stop()


    def stop(self):
        self.running = False