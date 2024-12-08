import statistics
from enum import Enum

from src.main.config.config import Config
from src.main.logging.logging_utilities import log_in_bold, \
    get_underline_string
from src.main.statistics.buffer_suggester import BufferSuggestions
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.statistics.track_performance import nanoseconds_to_milliseconds, \
    format_execution_time_number


class SpeedSuggester:
    PERFORMANCE_THRESHOLD: float = 1.2
    def __init__(self,
                    config: Config,
                    statistic_tracker: StatisticTracker,
                    buffer_suggester):
        self.config = config
        self.statistic_tracker = statistic_tracker
        self.buffer_suggester = buffer_suggester
        self.intended_producer_speed: float = self.get_intended_producer_speed()
        self.intended_consumer_speed: float = self.get_intended_consumer_speed()
        self.average_producer_speed: float = 0
        self.average_consumer_speed: float = 0
        self.producers_message: str = ""
        self.consumers_message: str = ""
        self.suggestions: list[SpeedSuggestions] = []

    def calculate(self):
        self.average_producer_speed = self.get_average_producer_speed()
        self.average_consumer_speed = self.get_average_consumer_speed()
        self.producers_message = self.get_producers_message()
        self.consumers_message = self.get_consumers_message()
        self.calculate_speed_suggestions()
        self.calculate_number_of_producers_suggestions()
        self.calculate_number_of_consumers_suggestions()

    def calculate_number_of_producers_suggestions(self):
        if self.get_mismatched_number_of_producers():
            self.suggestions.append(SpeedSuggestions.ADD_PRODUCERS)

    def calculate_number_of_consumers_suggestions(self):
        if self.get_mismatched_number_of_consumers():
            self.suggestions.append(SpeedSuggestions.ADD_CONSUMERS)

    def calculate_speed_suggestions(self):
        if self.exceeds_threshold(self.average_producer_speed, self.intended_producer_speed):
            self.suggestions.append(SpeedSuggestions.INCREASE_PRODUCER_SPEED)
        if self.exceeds_threshold(self.average_consumer_speed, self.intended_consumer_speed):
            self.suggestions.append(SpeedSuggestions.INCREASE_CONSUMER_SPEED)

    def get_should_increase_producer_speed(self) -> bool:
        return self.exceeds_threshold(self.average_producer_speed, self.intended_producer_speed)

    def get_should_increase_consumer_speed(self) -> bool:
        return self.exceeds_threshold(self.average_consumer_speed, self.intended_consumer_speed)

    def get_buffer_suggestion(self) -> BufferSuggestions:
        return self.buffer_suggester.suggestion

    def get_mismatched_number_of_producers(self) -> bool:
        if SpeedSuggestions.INCREASE_PRODUCER_SPEED in self.suggestions:
            return self.config.num_producers < self.config.num_consumers

    def get_mismatched_number_of_consumers(self) -> bool:
        if SpeedSuggestions.INCREASE_CONSUMER_SPEED in self.suggestions:
            return self.config.num_consumers < self.config.num_producers

    def show_suggestions(self):
        if len(self.suggestions) == 0:
            log_in_bold(SpeedSuggestions.NO_SUGGESTION.value)
        else:
            for suggestion in self.suggestions:
                log_in_bold(get_underline_string(suggestion.value))

    def get_average_producer_speed(self) -> float:
        mean_in_nanoseconds = statistics.mean(self.statistic_tracker.producer_throughput_list)
        return nanoseconds_to_milliseconds(mean_in_nanoseconds)

    def get_average_consumer_speed(self) -> float:
        mean_in_nanoseconds = statistics.mean(self.statistic_tracker.consumer_throughput_list)
        return nanoseconds_to_milliseconds(mean_in_nanoseconds)

    def get_intended_producer_speed(self) -> float:
        return sum(self.config.producer_speed_range) / 2

    def get_intended_consumer_speed(self) -> float:
        return sum(self.config.consumer_speed_range) / 2

    @staticmethod
    def exceeds_threshold(actual_speed: float, intended_speed: float) -> bool:
        return actual_speed > intended_speed * SpeedSuggester.PERFORMANCE_THRESHOLD

    def get_producers_message(self) -> str:
        intended_speed: str = format_execution_time_number(self.intended_producer_speed)
        actual_speed: str = format_execution_time_number(self.average_producer_speed)
        return f"""
        Intended producer average speed: {intended_speed} milliseconds.
        Actual producer average speed: {actual_speed} milliseconds"""


    def get_consumers_message(self) -> str:
        intended_speed: str = format_execution_time_number(self.intended_consumer_speed)
        actual_speed: str = format_execution_time_number(self.average_consumer_speed)
        return f"""
        Intended consumer average speed: {intended_speed} milliseconds.
        Actual consumer average speed: {actual_speed} milliseconds"""

    def show_statistics(self) -> None:
        log_in_bold(self.get_consumers_message())
        log_in_bold(self.get_producers_message())

class SpeedSuggestions(Enum):
    NO_SUGGESTION = "No changes are needed for the speed or amount of producers and consumers."
    ADD_PRODUCERS = "Add more producers."
    ADD_CONSUMERS = "Add more consumers."
    INCREASE_PRODUCER_SPEED = "Increase the speed of the producers."
    INCREASE_CONSUMER_SPEED = "Increase the speed of the consumers."
    DECREASE_PRODUCER_SPEED = "Decrease the speed of the producers."
    DECREASE_CONSUMER_SPEED = "Decrease the speed of the consumers."