import statistics
from enum import Enum
from typing import List

from src.main.config.config import Config
from src.main.logging.logging_utilities import log_in_bold, \
    get_underline_string
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.statistics.track_performance import nanoseconds_to_milliseconds, \
    format_execution_time_number
from src.main.suggestion.buffer_suggester import BufferSuggestions, \
    BufferSuggester


class SpeedSuggester:
    """
    This class analyzes the speed of producers and consumers, checks for
    performance mismatches or bottlenecks, and provides actionable suggestions
    to correct the issues. It uses statistical data and configuration ranges
    to determine the intended speeds, compare them with actual speeds, and
    give recommendations for speed adjustments or changes in the number of
    producers and consumers.

    :ivar config: The configuration parameters for speed and system settings.
    :type config: Config
    :ivar statistic_tracker: Tracks and provides producer and consumer
        throughput statistics.
    :type statistic_tracker: StatisticTracker
    :ivar buffer_suggester: Provides suggestions related to the buffer system.
    :type buffer_suggester: BufferSuggester
    :ivar intended_producer_speed: The target median speed for producers,
        based on configuration.
    :type intended_producer_speed: float
    :ivar intended_consumer_speed: The target median speed for consumers,
        based on configuration.
    :type intended_consumer_speed: float
    :ivar average_producer_speed: The calculated average speed for producers
        derived from statistical data.
    :type average_producer_speed: float
    :ivar average_consumer_speed: The calculated average speed for consumers
        derived from statistical data.
    :type average_consumer_speed: float
    :ivar producers_message: Information message regarding producer speeds.
    :type producers_message: str
    :ivar consumers_message: Information message regarding consumer speeds.
    :type consumers_message: str
    :ivar suggestions: A list of speed adjustments or changes suggested
        by the system.
    :type suggestions: List[SpeedSuggestions]
    """
    PERFORMANCE_THRESHOLD: float = 1.2
    def __init__(self,
                    config: Config,
                    statistic_tracker: StatisticTracker,
                    buffer_suggester: BufferSuggester):
        """
        Represents a manager to control and evaluate the producer and consumer
        speeds using provided configuration, trackers, and suggesters.

        :param config: The configuration object used to initialize the manager.
        :type config: Config
        :param statistic_tracker: Tracks statistical data for the simulation.
        :type statistic_tracker: StatisticTracker
        :param buffer_suggester: Suggests buffer-related adjustments.
        :type buffer_suggester: BufferSuggester
        """
        self.config: Config = config
        self.statistic_tracker: StatisticTracker = statistic_tracker
        self.buffer_suggester: BufferSuggester = buffer_suggester
        self.intended_producer_speed: float = self.get_intended_producer_speed()
        self.intended_consumer_speed: float = self.get_intended_consumer_speed()
        self.average_producer_speed: float = 0
        self.average_consumer_speed: float = 0
        self.producers_message: str = ""
        self.consumers_message: str = ""
        self.suggestions: List[SpeedSuggestions] = []

    def calculate(self) -> None:
        """
        Calculates various metrics and suggestions related to producer and
        consumer speeds and messages.

        :return: The method does not return any value.
        :rtype: None
        """
        self.average_producer_speed = self.get_average_producer_speed()
        self.average_consumer_speed = self.get_average_consumer_speed()
        self.producers_message = self.get_producers_message()
        self.consumers_message = self.get_consumers_message()
        self.calculate_speed_suggestions()
        self.calculate_number_of_producers_suggestions()
        self.calculate_number_of_consumers_suggestions()

    def calculate_number_of_producers_suggestions(self) -> None:
        """
        Analyzes mismatched number of producers based on specific conditions.
        If a mismatch is detected, it appends the corresponding suggestion to
        the list of suggestions.

        :return: The method does not return any value.
        :rtype: None
        """
        if self.get_mismatched_number_of_producers():
            self.suggestions.append(SpeedSuggestions.ADD_PRODUCERS)

    def calculate_number_of_consumers_suggestions(self) -> None:
        """
        Analyzes mismatched number of consumers based on specific conditions.
        If a mismatch is detected, it appends the corresponding suggestion to
        the list of suggestions.

        :return: The method does not return any value.
        :rtype: None
        """
        if self.get_mismatched_number_of_consumers():
            self.suggestions.append(SpeedSuggestions.ADD_CONSUMERS)

    def calculate_speed_suggestions(self) -> None:
        """
        Analyzes production and consumption speeds and appends appropriate
        speed adjustment suggestions if thresholds are exceeded.

        :return: The method does not return any value.
        :rtype: None
        """
        if self.exceeds_threshold(self.average_producer_speed, self.intended_producer_speed):
            self.suggestions.append(SpeedSuggestions.INCREASE_PRODUCER_SPEED)
        if self.exceeds_threshold(self.average_consumer_speed, self.intended_consumer_speed):
            self.suggestions.append(SpeedSuggestions.INCREASE_CONSUMER_SPEED)

    def get_should_increase_producer_speed(self) -> bool:
        """
        This method evaluates if the average producer speed surpasses the
        intended producer speed variability threshold. Returns a boolean
        indicating whether an increase is necessary.

        :return: A boolean indicating if the producer speed should be
        increased.
        :rtype: bool
        """
        return self.exceeds_threshold(self.average_producer_speed, self.intended_producer_speed)

    def get_should_increase_consumer_speed(self) -> bool:
        """
        This method evaluates if the average consumer speed surpasses the
        intended consumer speed variability threshold. Returns a boolean
        indicating whether an increase is necessary.

        :return: A boolean indicating if the consumer speed should be
        increased.
        :rtype: bool
        """
        return self.exceeds_threshold(self.average_consumer_speed, self.intended_consumer_speed)

    def get_buffer_suggestion(self) -> BufferSuggestions:
        """
        This method retrieves the buffer suggestion from the buffer suggester.

        :return: A buffer suggestion instance from the BufferSuggestions enum.
        :rtype: BufferSuggestions
        """
        return self.buffer_suggester.suggestion

    def get_mismatched_number_of_producers(self) -> bool:
        """
        Determines if there is a mismatch between the number of producers and
        consumers, based on the configured values and speed suggestions.

        :return: A boolean indicating whether the number of producers is less
            than the number of consumers under the specified conditions.
        :rtype: bool
        """
        if SpeedSuggestions.INCREASE_PRODUCER_SPEED in self.suggestions:
            return self.config.num_producers < self.config.num_consumers

    def get_mismatched_number_of_consumers(self) -> bool:
        """
        Determines if there is a mismatch between the number of consumers and
        producers, based on the configured values and speed suggestions.

        :return: A boolean indicating whether the number of consumers is less
            than the number of producers under the specified conditions.
        :rtype: bool
        """
        if SpeedSuggestions.INCREASE_CONSUMER_SPEED in self.suggestions:
            return self.config.num_consumers < self.config.num_producers

    def show_suggestions(self) -> None:
        """
        This method checks whether there are any suggestions available and
        displays them. If no suggestions are available, a default message is
        shown instead.

        :return: The method does not return any value.
        :rtype: None
        """
        has_no_suggestions: bool = len(self.suggestions) == 0
        if has_no_suggestions:
            log_in_bold(SpeedSuggestions.NO_SUGGESTION.value)
        else:
            for suggestion in self.suggestions:
                log_in_bold(get_underline_string(suggestion.value))

    def get_average_producer_speed(self) -> float:
        """
        Calculate the average producer speed in milliseconds.

        This method computes the mean value of the producer throughput
        in nanoseconds stored in `self.statistic_tracker.producer_throughput_list`
        and converts the result into milliseconds before returning.

        :returns: The average producer speed in milliseconds.
        :rtype: float
        """
        mean_in_nanoseconds = statistics.mean(self.statistic_tracker.producer_throughput_list)
        return nanoseconds_to_milliseconds(mean_in_nanoseconds)

    def get_average_consumer_speed(self) -> float:
        """
        Calculates the average consumer speed in milliseconds based on
        recorded throughput data.

        :return: The average consumer speed in milliseconds.
        :rtype: float
        """
        mean_in_nanoseconds = statistics.mean(self.statistic_tracker.consumer_throughput_list)
        return nanoseconds_to_milliseconds(mean_in_nanoseconds)

    def get_intended_producer_speed(self) -> float:
        """
        Calculate and return the intended producer speed.

        :return: The intended producer speed as a float value.
        :rtype: float
        """
        return sum(self.config.producer_speed_range) / 2

    def get_intended_consumer_speed(self) -> float:
        """
        Calculate the intended consumer speed based on the range.

        :return: The calculated intended consumer speed as a float.
        :rtype: float
        """
        return sum(self.config.consumer_speed_range) / 2

    @staticmethod
    def exceeds_threshold(actual_speed: float, intended_speed: float) -> bool:
        """
        Determines if the actual speed exceeds a specified performance
        threshold of the intended speed.

        :param actual_speed: The measured speed to evaluate.
        :type actual_speed: float
        :param intended_speed: The target speed to compare against.
        :type intended_speed: float
        :return: True if the actual speed exceeds the calculated threshold of
                 the intended speed, otherwise False.
        :rtype: bool
        """
        return actual_speed > intended_speed * SpeedSuggester.PERFORMANCE_THRESHOLD

    def get_producers_message(self) -> str:
        """
        Generates a formatted message detailing the intended and actual
        producer average speeds in milliseconds.

        :return: A formatted string containing the intended and actual
        producer average speeds in milliseconds.
        :rtype: str
        """
        intended_speed: str = format_execution_time_number(self.intended_producer_speed)
        actual_speed: str = format_execution_time_number(self.average_producer_speed)
        return f"""
        Intended producer average speed: {intended_speed} milliseconds.
        Actual producer average speed: {actual_speed} milliseconds"""


    def get_consumers_message(self) -> str:
        """
        Generates a formatted message detailing the intended and actual
        consumer average speeds in milliseconds.

        :return: A formatted string containing the intended and actual
        consumer average speeds in milliseconds.
        :rtype: str
        """
        intended_speed: str = format_execution_time_number(self.intended_consumer_speed)
        actual_speed: str = format_execution_time_number(self.average_consumer_speed)
        return f"""
        Intended consumer average speed: {intended_speed} milliseconds.
        Actual consumer average speed: {actual_speed} milliseconds"""

    def show_statistics(self) -> None:
        """
        Logs the statistics of consumers and producers in bold format.

        :return: This method does not return any value.
        :rtype: None
        """
        log_in_bold(self.get_consumers_message())
        log_in_bold(self.get_producers_message())

class SpeedSuggestions(Enum):
    """
    Represents various suggestions for optimizing the speed or
    count of producers and consumers in a system.

    :cvar NO_SUGGESTION: No changes are needed for the speed or amount of
     producers and consumers.
    :vartype NO_SUGGESTION: str
    :cvar ADD_PRODUCERS: Suggests adding more producers.
    :vartype ADD_PRODUCERS: str
    :cvar ADD_CONSUMERS: Suggests adding more consumers.
    :vartype ADD_CONSUMERS: str
    :cvar INCREASE_PRODUCER_SPEED: Suggests increasing the speed of the
     producers.
    :vartype INCREASE_PRODUCER_SPEED: str
    :cvar INCREASE_CONSUMER_SPEED: Suggests increasing the speed of the
     consumers.
    :vartype INCREASE_CONSUMER_SPEED: str
    :cvar DECREASE_PRODUCER_SPEED: Suggests decreasing the speed of the
     producers.
    :vartype DECREASE_PRODUCER_SPEED: str
    :cvar DECREASE_CONSUMER_SPEED: Suggests decreasing the speed of the
     consumers.
    :vartype DECREASE_CONSUMER_SPEED: str
    """
    NO_SUGGESTION: str = "No changes are needed for the speed or amount of producers and consumers."
    ADD_PRODUCERS: str = "Add more producers."
    ADD_CONSUMERS: str = "Add more consumers."
    INCREASE_PRODUCER_SPEED: str = "Increase the speed of the producers."
    INCREASE_CONSUMER_SPEED: str = "Increase the speed of the consumers."
    DECREASE_PRODUCER_SPEED: str = "Decrease the speed of the producers."
    DECREASE_CONSUMER_SPEED: str = "Decrease the speed of the consumers."