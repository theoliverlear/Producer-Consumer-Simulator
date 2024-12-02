import logging

from src.main.buffer.buffer_queue import BufferQueue
from src.main.config.config import Config
from src.main.thread.processor.lock.mutex_lock import MutexLock
from src.main.thread.thread_manager import ThreadManager


class Simulator:
    def __init__(self, config: Config):
        self.config = config
        logging.info("Starting simulator")
        lock = MutexLock()
        self.buffer = BufferQueue(config.buffer_size, lock)
        self.thread_manager = ThreadManager(
            num_producers=config.num_producers,
            num_consumers=config.num_consumers,
            consumer_speed_range=config.consumer_speed_range,
            producer_speed_range=config.producer_speed_range,
            buffer=self.buffer,
            num_items_to_process=config.num_items_to_process
        )
        self.is_running = False

    def simulate(self) -> None:
        self.start()
        try:
            self.thread_manager.stop_all()
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.stop()

    def start(self) -> None:
        self.is_running = True
        self.thread_manager.start_all()

    def stop(self) -> None:
        self.is_running = False
        self.thread_manager.stop_all()

    def show_suggestions(self) -> None:
        pass

    def show_efficiency(self) -> None:
        pass

