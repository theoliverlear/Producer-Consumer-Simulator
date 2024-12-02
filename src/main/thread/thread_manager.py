from src.main.thread.processor.processor import Processor


class ThreadManager:
    def __init__(self, num_producers: int,
                 num_consumers: int,
                 consumer_speed_range: tuple[int, int],
                 producer_speed_range: tuple[int, int]):
        self.producers = self.initialize_processors(num_producers, producer_speed_range)
        self.consumers = self.initialize_processors(num_consumers, consumer_speed_range)

    @staticmethod
    def initialize_processors(num_processors, processor_speed_range):
        return [Processor(processor_speed_range[0], processor_speed_range[1]) for
                i in range(num_processors)]

