from enum import Enum

from src.main.config.config import Config
from src.main.logging.logging_utilities import log_in_bold, \
    get_underline_string
from src.main.statistics.statistic_tracker import StatisticTracker


class BufferSuggester:
    """
    The `BufferSuggester` class evaluates system buffer usage statistics
    and provides suggestions to increase, decrease, or maintain the buffer
    size.

    :ivar config: Configuration object containing system-level settings.
    :type config: Config
    :ivar statistic_tracker: Tracker for buffer statistics such as full and
     empty buffer occurrences and the number of items to process.
    :type statistic_tracker: StatisticTracker
    :ivar buffer_size: Buffer size obtained from the configuration.
    :type buffer_size: int
    :ivar num_full_buffer: Number of occurrences when the buffer has been
        full during its operation.
    :type num_full_buffer: int
    :ivar num_empty_buffer: Number of occurrences when the buffer has been
        empty during its operation.
    :type num_empty_buffer: int
    :ivar num_items_to_process: Total number of items processed by the system.
    :type num_items_to_process: int
    :ivar suggestion: A buffer suggestion, indicating whether to increase,
     decrease, or maintain the buffer size.
    :type suggestion: BufferSuggestions
    """
    BUFFER_CHANGE_THRESHOLD: float = 0.1
    BUFFER_SIZE_THRESHOLD: float = 0.65
    def __init__(self,
                    config: Config,
                    statistic_tracker: StatisticTracker):
        """
        Handles the initialization and management of buffer-related variables.

        :param config: Configuration object containing buffer-related
        settings.
        :type config: Config
        :param statistic_tracker: Object used for tracking runtime statistics.
        :type statistic_tracker: StatisticTracker
        :ivar config: Configuration object containing system-level settings.
        :ivar statistic_tracker: Object tracking runtime statistics.
        :ivar buffer_size: Size of the buffer, sourced from the config
        attribute.
        :ivar num_full_buffer: Counter for the number of times buffer was
        full.
        :ivar num_empty_buffer: Counter for the number of times buffers was
        empty.
        :ivar num_items_to_process: Total number of items to process in the
        buffer.
        :ivar suggestion: Buffer suggestion of type BufferSuggestions.
        """
        self.config: Config = config
        self.statistic_tracker: StatisticTracker = statistic_tracker
        self.buffer_size: int = config.buffer_size
        self.num_full_buffer: int = 0
        self.num_empty_buffer: int = 0
        self.num_items_to_process: int = 0
        self.suggestion: BufferSuggestions = BufferSuggestions.KEEP_BUFFER_SIZE

    def calculate(self) -> None:
        """
        Calculates buffer size adjustment suggestions based on the buffer usage
        statistics, such as the number of full and empty buffers and items to
        process.

        :return: This method does not return any value.
        :rtype: None
        """
        self.num_full_buffer = self.statistic_tracker.num_full_buffer
        self.num_empty_buffer = self.statistic_tracker.num_empty_buffer
        self.num_items_to_process = self.statistic_tracker.num_items_to_process
        if self.should_increase_buffer_size():
            self.suggestion = BufferSuggestions.INCREASE_BUFFER_SIZE
        elif self.should_decrease_buffer_size():
            self.suggestion = BufferSuggestions.DECREASE_BUFFER_SIZE
        else:
            self.suggestion = BufferSuggestions.KEEP_BUFFER_SIZE
        self.calculate_reduction_suggestion()

    def should_increase_buffer_size(self) -> bool:
        """
        Determines if the buffer size should be increased based on the
        processing requirements and the tracked statistics.

        :return: A boolean indicating whether the buffer size needs to be
         increased.
        :rtype: bool
        """
        return self.num_items_to_process * BufferSuggester.BUFFER_CHANGE_THRESHOLD < self.num_full_buffer

    def should_decrease_buffer_size(self) -> bool:
        """
        Determines if the buffer size should be decreased based on the
        comparison of the product of the number of items to process and a
        predefined buffer change threshold with the number of empty buffers.

        :return: A boolean indicating whether the buffer size should be decreased.
        :rtype: bool
        """
        return self.num_items_to_process * BufferSuggester.BUFFER_CHANGE_THRESHOLD < self.num_empty_buffer

    def should_keep_buffer_size(self) -> bool:
        """
        Determines whether the buffer size should remain unchanged.

        :return: A boolean value indicating whether the buffer size should
            remain unchanged.
        :rtype: bool
        """
        return not self.should_increase_buffer_size() and not self.should_decrease_buffer_size()

    def calculate_reduction_suggestion(self) -> None:
        """
        Calculates and updates the buffer size reduction suggestion.

        :return: This method does not return any value.
        :rtype: None
        """
        is_keep_same: bool = self.suggestion == BufferSuggestions.KEEP_BUFFER_SIZE
        is_over_size_threshold: bool = self.buffer_size * BufferSuggester.BUFFER_SIZE_THRESHOLD > self.num_items_to_process
        if is_keep_same and is_over_size_threshold:
            self.suggestion = BufferSuggestions.BUFFER_SIZE_MAY_BE_REDUCED

    def show_statistics(self) -> None:
        """
        Logs the buffer statistics to display the frequency of buffer states
        during processing. It calculates the ratio of empty or full buffer
        occurrences to the total number of items processed, formats the
        statistics, and logs them in bold.

        :return: None
        """
        empty_to_item_ratio: float = (self.num_empty_buffer /
                                      self.num_items_to_process)
        full_to_item_ratio: float = (self.num_full_buffer /
                                     self.num_items_to_process)
        buffer_statistics: str = f"""
        Number of times buffer was empty: {self.num_empty_buffer} - {empty_to_item_ratio}:1 item
        Number of times buffer was full: {self.num_full_buffer} - {full_to_item_ratio}:1 item"""
        log_in_bold(buffer_statistics)

    def show_suggestions(self) -> None:
        """
        Logs suggestion values in a formatted string with bold and underline
        styles.

        :return: This method does not return any value.
        :rtype: None
        """
        log_in_bold(get_underline_string(self.suggestion.value))

class BufferSuggestions(Enum):
    """
    Enumeration representing suggestions for buffer size adjustments.

    :cvar INCREASE_BUFFER_SIZE: Suggests increasing the buffer size.
    :type INCREASE_BUFFER_SIZE: str
    :cvar DECREASE_BUFFER_SIZE: Suggests decreasing the buffer size.
    :type DECREASE_BUFFER_SIZE: str
    :cvar KEEP_BUFFER_SIZE: Suggests maintaining the current buffer size.
    :type KEEP_BUFFER_SIZE: str
    :cvar BUFFER_SIZE_MAY_BE_REDUCED: Indicates that, optionally, the buffer
        size could be reduced, depending on requirements.
    :type BUFFER_SIZE_MAY_BE_REDUCED: str
    """
    INCREASE_BUFFER_SIZE: str = "Buffer size should be increased."
    DECREASE_BUFFER_SIZE: str = "Buffer size should be decreased."
    KEEP_BUFFER_SIZE: str = "Buffer size should be kept the same."
    BUFFER_SIZE_MAY_BE_REDUCED: str = "Buffer size may be reduced."