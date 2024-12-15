import logging
import time

from src.main.buffer.buffer import Buffer
from src.main.buffer.buffer_queue import BufferQueue
from src.main.config.config import Config
from src.main.logging.logging_utilities import log_in_bold
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.suggestion.suggester import Suggester
from src.main.thread.processor.lock.mutex_lock import MutexLock
from src.main.thread.thread_manager import ThreadManager


class Simulator:
    """
    Handles the main execution of the Producer-Consumer Simulator.

    This class is responsible for initializing and orchestrating various
    components such as buffer management, thread handling, and statistical
    tracking. Its purpose is to simulate a producer-consumer runtime with
    customizable configurations.

    :ivar config: Configuration settings for the simulator.
    :type config: Config
    :ivar statistic_tracker: Tracks statistics and metrics during simulation.
    :type statistic_tracker: StatisticTracker
    :ivar buffer: Buffer implementation for producer-consumer data exchange.
    :type buffer: Buffer
    :ivar thread_manager: Manages producer and consumer threads.
    :type thread_manager: ThreadManager
    :ivar suggester: Provides suggestions post-simulation if enabled.
    :type suggester: Suggester
    :ivar is_running: Indicates whether the simulation is currently active.
    :type is_running: bool
    """
    def __init__(self, config: Config):
        """
        This class initializes and configures the simulator environment,
        setting up required components such as statistics tracker, buffer,
        thread manager, and optional suggester based on the given
        configuration.

        :ivar config: The configuration settings for the simulator.
        :type config: Config
        :ivar statistic_tracker: Object that tracks simulation statistics like
        buffer state and processing speed.
        :type statistic_tracker: StatisticTracker
        :ivar buffer: Buffer used for storing items.
        :type buffer: Buffer
        :ivar thread_manager: Manages threads for producers and consumers.
        :type thread_manager: ThreadManager
        :ivar suggester: Optional component for managing the suggestions
        feature.
        :type suggester: Suggester
        :ivar is_running: Boolean indicating whether the simulation is
        running.
        :type is_running: bool
        """
        self.config: Config = config
        logging.info("Starting simulator")
        lock: MutexLock = MutexLock()
        self.statistic_tracker: StatisticTracker = StatisticTracker(config.num_items_to_process)
        self.buffer: Buffer = BufferQueue(config.buffer_size, lock, self.statistic_tracker)
        self.thread_manager: ThreadManager = ThreadManager(
            num_producers=config.num_producers,
            num_consumers=config.num_consumers,
            consumer_speed_range=config.consumer_speed_range,
            producer_speed_range=config.producer_speed_range,
            buffer=self.buffer,
            num_items_to_process=config.num_items_to_process,
            statistic_tracker=self.statistic_tracker
        )
        if config.suggestions:
            self.suggester: Suggester = Suggester(config, self.statistic_tracker)
        self.is_running: bool = False

    def simulate(self) -> None:
        """
        This method orchestrates the entire lifecycle of a simulation. It
        includes initial setup, statistics tracking, thread management,
        handling interruptions, and performing cleanup actions. Suggestions
        are displayed if configured.

        :raises KeyboardInterrupt: If a keyboard interrupt signal is received
        during thread join.
        :rtype: None
        :return: No return value. The method modifies the runtime state of the
         system.
        """
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
        """
        Starts the necessary threads for managing operations and sets the
        running state to True.

        :return: None
        """
        self.is_running = True
        self.thread_manager.start_all()

    def stop(self) -> None:
        """
        Stops the current running process by setting the running state to
        False and joining all threads.

        :return: None
        """
        self.is_running = False
        self.thread_manager.join_all()

    def show_ending_message(self) -> None:
        """

        This function formats and displays a message that the simulation has
        completed. Optionally, it informs the user about how to enable
        suggestions if they were not used during the simulation.

        :returns: None
        """
        newline_with_tabs: str = "\n\t\t"
        ending_message: str = (f"{newline_with_tabs}The simulation has ended."
                               f" Thank you for using the Producer-Consumer"
                               f" Simulator!")
        if not self.config.suggestions:
            ending_message += (f"{newline_with_tabs}Run the simulator with "
                               f"the '-s' flag to see suggestions.")
        log_in_bold(ending_message)

    def show_suggestions(self) -> None:
        """
        This method invokes the `show_suggestions` method of the `suggester`
        object to display configuration suggestions.

        :return: None
        """
        self.suggester.show_suggestions()