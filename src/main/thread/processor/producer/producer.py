import logging
import random
import time

from src.main.buffer.buffer import Buffer
from src.main.buffer.full_buffer_exception import FullBufferException
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.statistics.track_performance import track_producer_performance
from src.main.thread.processor.processor import Processor


class Producer(Processor):
    """
    Manages the production of items and their interaction with a shared
    buffer in a simulation environment.

    :ivar name: Name of the producer instance. Initialized with a unique id.
    :type name: str
    """
    def __init__(self,
                 id: int,
                 speed_floor: int,
                 speed_ceiling: int,
                 buffer: Buffer,
                 num_items_to_process: int,
                 statistic_tracker: StatisticTracker):
        """
        Initialize a Producer instance with specific attributes including
        identifiers, speed constraints, a shared buffer, and a tracker for
        statistics.

        :param id: Unique identifier for the producer.
        :type id: int
        :param speed_floor: Minimum speed of production.
        :type speed_floor: int
        :param speed_ceiling: Maximum speed of production.
        :type speed_ceiling: int
        :param buffer: Shared buffer where produced items will be stored.
        :type buffer: Buffer
        :param num_items_to_process: Total number of items the producer should
         create.
        :type num_items_to_process: int
        :param statistic_tracker: Tracks and records production-related
        statistics.
        :type statistic_tracker: StatisticTracker
        """
        super().__init__(id,
                         speed_floor,
                         speed_ceiling,
                         buffer,
                         num_items_to_process,
                         statistic_tracker)
        self.name = f"Producer-{id}"

    @staticmethod
    def get_random_number() -> int:
        """
        Generates a random integer within the range [1, 100].

        :return: A random integer between 1 and 100 inclusive.
        :rtype: int
        """
        return random.randint(1, 100)

    def run(self) -> None:
        """
        This method initiates and runs a continuous execution loop that keeps
        processing items until the stopping condition is met. The loop starts
        by setting the `running` attribute to True, continues execution by
        calling the `process_item` repeatedly while `should_run` evaluates
        to True, and stops by invoking the `stop` method.

        :return: This method does not return any value.
        :rtype: None
        """
        self.running = True
        while self.should_run():
            self.process_item()
        self.stop()

    @track_producer_performance
    def process_item(self) -> None:
        """
        Processes an item by generating a random number, enqueuing it into
        the buffer, and reducing the counter for remaining items to process.
        Handles `FullBufferException` by sleeping for a short duration and
        then attempting to reprocess.

        :raises FullBufferException: If the buffer is full and unable to
            enqueue the generated random number.
        :return: This method does not return any value.
        :rtype: None
        """
        try:
            random_number: int = self.get_random_number()
            logging.debug(f"Enqueued number: {random_number}")
            self.buffer.enqueue(random_number)
            self.num_items_to_process -= 1
            logging.debug(f"Items remaining: {self.num_items_to_process}")
        except FullBufferException:
            time.sleep(0.01)
            return
        self.simulate_processing()

    def stop(self):
        """
        Stops the producer by setting its running status to False.

        :return: This method does not return any value.
        :rtype: None
        """
        num_items_remaining: int = (self.statistic_tracker.num_items_to_process -
                                    self.statistic_tracker.items_produced)
        num_remaining_string: str = f"{num_items_remaining}"
        logging.debug(f"Producer {self.id} stopped. {num_remaining_string} items remaining.")
        self.running = False