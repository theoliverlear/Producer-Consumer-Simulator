from enum import Enum

from src.main.config.config import Config
from src.main.logging.logging_utilities import log_in_bold, \
    get_underline_string
from src.main.statistics.statistic_tracker import StatisticTracker


class BufferSuggester:
    BUFFER_CHANGE_THRESHOLD: float = 0.1
    BUFFER_SIZE_THRESHOLD: float = 0.65
    def __init__(self,
                    config: Config,
                    statistic_tracker: StatisticTracker):
        self.config = config
        self.statistic_tracker = statistic_tracker
        self.buffer_size: int = config.buffer_size
        self.num_full_buffer: int = 0
        self.num_empty_buffer: int = 0
        self.num_items_to_process: int = 0
        self.suggestion: BufferSuggestions = BufferSuggestions.KEEP_BUFFER_SIZE

    def calculate(self):
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
        return self.num_items_to_process * BufferSuggester.BUFFER_CHANGE_THRESHOLD < self.num_full_buffer

    def should_decrease_buffer_size(self) -> bool:
        return self.num_items_to_process * BufferSuggester.BUFFER_CHANGE_THRESHOLD < self.num_empty_buffer

    def should_keep_buffer_size(self) -> bool:
        return not self.should_increase_buffer_size() and not self.should_decrease_buffer_size()

    def calculate_reduction_suggestion(self):
        is_keep_same: bool = self.suggestion == BufferSuggestions.KEEP_BUFFER_SIZE
        is_over_size_threshold: bool = self.buffer_size * BufferSuggester.BUFFER_SIZE_THRESHOLD > self.num_items_to_process
        if is_keep_same and is_over_size_threshold:
            self.suggestion = BufferSuggestions.BUFFER_SIZE_MAY_BE_REDUCED

    def show_statistics(self):
        empty_to_item_ratio = self.num_empty_buffer / self.num_items_to_process
        full_to_item_ratio = self.num_full_buffer / self.num_items_to_process
        buffer_statistics = f"""
        Number of times buffer was empty: {self.num_empty_buffer} - {empty_to_item_ratio}:1 item
        Number of times buffer was full: {self.num_full_buffer} - {full_to_item_ratio}:1 item"""
        log_in_bold(buffer_statistics)

    def show_suggestions(self):
        log_in_bold(get_underline_string(self.suggestion.value))

class BufferSuggestions(Enum):
    INCREASE_BUFFER_SIZE = "Buffer size should be increased."
    DECREASE_BUFFER_SIZE = "Buffer size should be decreased."
    KEEP_BUFFER_SIZE = "Buffer size should be kept the same."
    BUFFER_SIZE_MAY_BE_REDUCED = "Buffer size may be reduced."