class Config:
    def __init__(self,
                 buffer_size: int,
                 num_items_to_process: int,
                 num_producers: int,
                 num_consumers: int,
                 consumer_speed_range: tuple[int, int],
                 producer_speed_range: tuple[int, int],
                 verbose: bool,
                 suggestions: bool):
        self.buffer_size = buffer_size
        self.num_items_to_process = num_items_to_process
        self.num_producers = num_producers
        self.num_consumers = num_consumers
        self.consumer_speed_range = consumer_speed_range
        self.producer_speed_range = producer_speed_range
        self.verbose = verbose
        self.suggestions = suggestions

    def __str__(self):
        return (f"Config(buffer_size={self.buffer_size},"
                f" num_items_to_process={self.num_items_to_process},"
                f" num_producers={self.num_producers},"
                f" num_consumers={self.num_consumers},"
                f" consumer_speed_range={self.consumer_speed_range},"
                f" producer_speed_range={self.producer_speed_range},"
                f" verbose={self.verbose}, suggestions={self.suggestions})")