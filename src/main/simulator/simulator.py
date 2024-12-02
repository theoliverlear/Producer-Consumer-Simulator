from src.main.buffer.buffer_queue import BufferQueue
from src.main.config.config import Config
from src.main.logging.setup_logging import setup_logging
from src.main.thread.thread_manager import ThreadManager


class Simulator:
    def __init__(self, config: Config):
        self.config = config
        setup_logging(config.verbose)
        self.buffer = BufferQueue(config.buffer_size, config.num_items_to_process)
        self.thread_manager = ThreadManager(
            num_producers=config.num_producers,
            num_consumers=config.num_consumers,
            consumer_speed_range=config.consumer_speed_range,
            producer_speed_range=config.producer_speed_range,
            buffer=self.buffer
        )
        self.is_running = False

    def simulate(self) -> None:
        self.start()
        # TODO: Add business logic
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

