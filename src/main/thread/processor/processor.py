import random
import threading
import time
from abc import ABC, abstractmethod

from src.main.buffer.buffer import Buffer


class Processor(ABC, threading.Thread):
    def __init__(self, speed_floor: int,
                 speed_ceiling: int,
                 buffer: Buffer,
                 num_items_to_process: int):
        super().__init__()
        self.speed_floor = speed_floor
        self.speed_ceiling = speed_ceiling
        self.buffer = buffer
        self.running = False
        self.num_items_to_process = num_items_to_process

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def get_random_speed(self):
        return random.randint(self.speed_floor, self.speed_ceiling)
    
    def simulate_processing(self):
        processing_time = self.get_random_speed()
        time.sleep(processing_time / 1000)
