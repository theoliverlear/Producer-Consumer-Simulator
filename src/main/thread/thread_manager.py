from src.main.buffer.buffer import Buffer
from src.main.thread.processor.consumer.consumer import Consumer
from src.main.thread.processor.producer.producer import Producer


class ThreadManager:
    def __init__(self, num_producers: int,
                 num_consumers: int,
                 consumer_speed_range: tuple[int, int],
                 producer_speed_range: tuple[int, int],
                 buffer: Buffer):
        self.num_producers = num_producers
        self.num_consumers = num_consumers
        self.producer_speed_range = producer_speed_range
        self.consumer_speed_range = consumer_speed_range
        self.producers = self.initialize_producers()
        self.consumers = self.initialize_consumers()
        self.buffer = buffer

    def initialize_producers(self):
        return [Producer(self.producer_speed_range[0], self.producer_speed_range[1], self.buffer) for _ in range(self.num_producers)]

    def initialize_consumers(self):
        return [Consumer(self.consumer_speed_range[0], self.consumer_speed_range[1], self.buffer) for _ in range(self.num_consumers)]


    def start_producers(self):
        for producer in self.producers:
            producer.start()

    def start_consumers(self):
        for consumer in self.consumers:
            consumer.start()

    def start_all(self):
        self.start_producers()
        self.start_consumers()

    def stop_producers(self):
        for producer in self.producers:
            producer.join()

    def stop_consumers(self):
        for consumer in self.consumers:
            consumer.join()

    def stop_all(self):
        self.stop_producers()
        self.stop_consumers()