from src.main.config.config import Config
from src.main.statistics.statistic_tracker import StatisticTracker
from src.main.suggestion.buffer_suggester import BufferSuggester
from src.main.suggestion.speed_suggester import SpeedSuggester


class Suggester:
    def __init__(self,
                 config: Config,
                 statistic_tracker: StatisticTracker):
        self.config = config
        self.statistic_tracker = statistic_tracker
        self.buffer_suggester = BufferSuggester(config, statistic_tracker)
        self.speed_suggester = SpeedSuggester(config, statistic_tracker, self.buffer_suggester)

    def show_suggestions(self) -> None:
        self.show_buffer_suggestions()
        self.show_speed_suggestions()

    def show_buffer_suggestions(self) -> None:
        self.buffer_suggester.calculate()
        self.buffer_suggester.show_statistics()
        self.buffer_suggester.show_suggestions()

    def show_speed_suggestions(self) -> None:
        self.speed_suggester.calculate()
        self.speed_suggester.show_statistics()
        self.speed_suggester.show_suggestions()
