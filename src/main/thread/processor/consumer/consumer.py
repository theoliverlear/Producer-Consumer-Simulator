from abc import ABC

from src.main.buffer.buffer import Buffer
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.thread.processor.processor import Processor


class Consumer(Processor, ABC):
    def __init__(self, speed_floor: int, speed_ceiling: int, buffer: Buffer):
        super().__init__(speed_floor, speed_ceiling, buffer)

    def run(self) -> None:
        while self.running:
            try:
                self.buffer.dequeue()
            except EmptyBufferException:
                pass
            super().simulate_processing()


    def stop(self):
        self.running = False