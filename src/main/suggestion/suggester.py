from src.main.config.config import Config
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.suggestion.buffer_suggester import BufferSuggester
from src.main.suggestion.speed_suggester import SpeedSuggester


class Suggester:
    """
    The Suggester class provides functionality to manage and display
    suggestions by utilizing buffer and speed suggesters. It acts as
    a coordinator for the suggestion-related processes.

    :ivar config: Configuration settings for the simulation.
    :type config: Config
    :ivar statistic_tracker: Tracks and provides statistical data.
    :type statistic_tracker: StatisticTracker
    :ivar buffer_suggester: Handles buffer-related suggestions.
    :type buffer_suggester: BufferSuggester
    :ivar speed_suggester: Handles speed-related suggestions.
    :type speed_suggester: SpeedSuggester
    """
    def __init__(self,
                 config: Config,
                 statistic_tracker: StatisticTracker):
        """
        Initializes the Suggester with configuration and statistical tracking.

        :param config: Configuration object containing settings for the
         application.
        :type config: Config
        :param statistic_tracker: Object responsible for tracking statistical
         data used by the suggesters.
        :type statistic_tracker: StatisticTracker
        """
        self.config: Config = config
        self.statistic_tracker: StatisticTracker = statistic_tracker
        self.buffer_suggester: BufferSuggester = BufferSuggester(config, statistic_tracker)
        self.speed_suggester: SpeedSuggester = SpeedSuggester(config, statistic_tracker, self.buffer_suggester)

    def show_suggestions(self) -> None:
        """
        Displays suggestions to the user.

        :return: The method does not return any value.
        :rtype: None
        """
        self.show_buffer_suggestions()
        self.show_speed_suggestions()

    def show_buffer_suggestions(self) -> None:
        """
        Calculates buffer suggestions, displays related statistics,
        and shows suggestions for a buffer.

        :return: The method does not return any value.
        :rtype: None
        """
        self.buffer_suggester.calculate()
        self.buffer_suggester.show_statistics()
        self.buffer_suggester.show_suggestions()

    def show_speed_suggestions(self) -> None:
        """
        Calculates speed suggestions, displays related statistics,
        and shows suggestions for speed.

        :return: The method does not return any value.
        :rtype: None
        """
        self.speed_suggester.calculate()
        self.speed_suggester.show_statistics()
        self.speed_suggester.show_suggestions()
