import logging
import time
from abc import ABC

from src.main.buffer.buffer import Buffer
from src.main.buffer.empty_buffer_exception import EmptyBufferException
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.statistics.track_performance import track_consumer_performance
from src.main.thread.processor.processor import Processor


class Consumer(Processor, ABC):
    """
    Consumer class responsible for consuming items from a shared buffer.

    :ivar name: The name of the consumer, formatted as "Consumer-{id}".
    :type name: str
    :ivar running: A flag indicating whether the consumer is actively running.
    :type running: bool
    """
    def __init__(self,
                 id: int,
                 speed_floor: int,
                 speed_ceiling: int,
                 buffer: Buffer,
                 num_items_to_process: int,
                 statistic_tracker: StatisticTracker):
        """
        Initializes a Consumer instance with specific attributes including
        identifiers, speed constraints, a shared buffer, processing
        requirements, and a tracker for statistics.


        :param id: Unique identifier for the consumer.
        :type id: int
        :param speed_floor: Minimum processing speed of the consumer.
        :type speed_floor: int
        :param speed_ceiling: Maximum processing speed of the consumer.
        :type speed_ceiling: int
        :param buffer: Shared buffer from which the consumer processes items.
        :type buffer: Buffer
        :param num_items_to_process: Total number of items the consumer will
        process.
        :type num_items_to_process: int
        :param statistic_tracker: Tracker for collecting processing
        statistics.
        :type statistic_tracker: StatisticTracker
        """
        super().__init__(id,
                         speed_floor,
                         speed_ceiling,
                         buffer,
                         num_items_to_process,
                         statistic_tracker)
        self.name = f"Consumer-{id}"

    def run(self) -> None:
        """
        Controls the execution of a running process.

        :return: This method does not return any value.
        :rtype: None
        """
        self.running = True
        while self.should_run():
            self.process_item()
        self.stop()

    @track_consumer_performance
    def process_item(self) -> None:
        """
        Processes an item from the buffer by dequeuing it and updating the
        number of items to process. If the buffer is empty, logs relevant
        details about remaining items, checks if the processing is completed,
        and stops if required.

        :return: This method does not return any value.
        :rtype: None
        """
        try:
            dequeued_number: int = self.buffer.dequeue()
            logging.debug(f"Dequeued number: {dequeued_number}")
            self.num_items_to_process -= 1
            logging.debug(f"Items remaining: {self.num_items_to_process}")
            self.simulate_processing()
        except EmptyBufferException:
            num_remaining_items: int = (self.statistic_tracker.num_items_to_process
                                        - self.statistic_tracker.items_produced)
            num_remaining_string: str = f"{num_remaining_items}"
            logging.debug(f"Buffer is empty. {num_remaining_string} items remaining.")
            has_completed_processing: bool = (self.statistic_tracker.items_produced ==
                                              self.statistic_tracker.num_items_to_process)
            if has_completed_processing:
                self.stop()
            else:
                time.sleep(0.01)
            return

    def stop(self):
        """
        Provides functionality to stop a running process by altering its internal
        state.

        :return: This method does not return any value.
        :rtype: None
        """
        self.running = False