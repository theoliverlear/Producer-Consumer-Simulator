
import random


from src.main.buffer.buffer import Buffer
from src.main.buffer.full_buffer_exception import FullBufferException
from src.main.thread.processor.processor import Processor


class Producer(Processor):
    def __init__(self, speed_floor: int, speed_ceiling: int, buffer: Buffer):
        super().__init__(speed_floor, speed_ceiling, buffer)

    @staticmethod
    def get_random_number() -> int:
        return random.randint(1, 100)


    def run(self) -> None:
        while self.running:
            random_number: int = self.get_random_number()
            try:
                self.buffer.enqueue(random_number)
            except FullBufferException:
                pass
            super().simulate_processing()

    def stop(self):
        self.running = False