import logging
import time

from src.main.buffer.buffer_queue import BufferQueue
from src.main.config.config import Config
from src.main.logging.logging_utilities import log_in_bold
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.suggestion.suggester import Suggester
from src.main.thread.processor.lock.mutex_lock import MutexLock
from src.main.thread.thread_manager import ThreadManager


class Simulator:
    def __init__(self, config: Config):
        self.config = config
        logging.info("Starting simulator")
        lock = MutexLock()
        self.statistic_tracker = StatisticTracker(config.num_items_to_process)
        self.buffer = BufferQueue(config.buffer_size, lock, self.statistic_tracker)
        self.thread_manager = ThreadManager(
            num_producers=config.num_producers,
            num_consumers=config.num_consumers,
            consumer_speed_range=config.consumer_speed_range,
            producer_speed_range=config.producer_speed_range,
            buffer=self.buffer,
            num_items_to_process=config.num_items_to_process,
            statistic_tracker=self.statistic_tracker
        )
        if config.suggestions:
            self.suggester = Suggester(config, self.statistic_tracker)
        self.is_running = False

    def simulate(self) -> None:
        self.start()
        self.statistic_tracker.start()
        time.sleep(1)
        try:
            if self.thread_manager.threads_started:
                self.thread_manager.join_all()
        except KeyboardInterrupt:
            self.stop()
        finally:
            if self.is_running:
                self.stop()
            self.statistic_tracker.stop()
            if self.config.suggestions:
                self.suggester.show_suggestions()
            self.show_ending_message()

    def start(self) -> None:
        self.is_running = True
        self.thread_manager.start_all()

    def stop(self) -> None:
        self.is_running = False
        self.thread_manager.join_all()

    def show_ending_message(self) -> None:
        newline_with_tabs: str = "\n\t\t"
        ending_message: str = (f"{newline_with_tabs}The simulation has ended."
                               f" Thank you for using the Producer-Consumer"
                               f" Simulator!")
        if not self.config.suggestions:
            ending_message += (f"{newline_with_tabs}Run the simulator with "
                               f"the '-s' flag to see suggestions.")
        log_in_bold(ending_message)

    def show_suggestions(self) -> None:
        self.suggester.show_suggestions()