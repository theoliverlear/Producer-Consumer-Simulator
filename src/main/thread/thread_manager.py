from typing import List

from src.main.buffer.buffer import Buffer
from src.main.thread.processor.consumer.consumer import Consumer
from src.main.thread.processor.producer.producer import Producer


class ThreadManager:
    def __init__(self, num_producers: int,
                 num_consumers: int,
                 consumer_speed_range: tuple[int, int],
                 producer_speed_range: tuple[int, int],
                 buffer: Buffer,
                 num_items_to_process: int):
        self.buffer = buffer
        self.num_items_to_process = num_items_to_process
        self.num_producers = num_producers
        self.num_consumers = num_consumers
        self.producer_speed_range = producer_speed_range
        self.consumer_speed_range = consumer_speed_range
        self.producers = self.initialize_producers()
        self.consumers = self.initialize_consumers()

    def get_num_items_to_produce(self):
        items_per_producer: int = self.num_items_to_process // self.num_producers
        leftover_items: int = self.num_items_to_process % self.num_producers
        return items_per_producer, leftover_items

    def get_num_items_to_consume(self):
        items_per_consumer: int = self.num_items_to_process // self.num_consumers
        leftover_items: int = self.num_items_to_process % self.num_consumers
        return items_per_consumer, leftover_items

    def initialize_producers(self):
        items_per_producer, leftover_items = self.get_num_items_to_produce()
        producers: List[Producer] = []
        for i in range(self.num_producers):
            items_to_produce = items_per_producer + (1 if i < leftover_items else 0)
            producers.append(Producer(self.producer_speed_range[0], self.producer_speed_range[1], self.buffer, items_to_produce))
        return producers


    def initialize_consumers(self):
        items_per_consumer, leftover_items = self.get_num_items_to_consume()
        consumers: List[Consumer] = []
        for i in range(self.num_consumers):
            items_to_consume = items_per_consumer + (1 if i < leftover_items else 0)
            consumers.append(Consumer(self.consumer_speed_range[0], self.consumer_speed_range[1], self.buffer, items_to_consume))
        return consumers


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