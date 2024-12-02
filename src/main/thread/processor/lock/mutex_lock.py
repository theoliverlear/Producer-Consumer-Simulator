import itertools
import logging
import threading
from threading import Condition
from typing import List

from src.main.thread.processor.lock.lock_state import LockState


class MutexLock:
    def __init__(self):
        self.lock_state: LockState = LockState.AVAILABLE
        self.condition: Condition = threading.Condition()
        self.queue_counter: itertools.count[int] = itertools.count()
        self.wait_queue: List[int] = []

    def get_next_queue_number(self) -> int:
        return next(self.queue_counter)


    def lock(self):
        self.lock_state = LockState.UNAVAILABLE

    def unlock(self):
        self.lock_state = LockState.AVAILABLE

    def is_locked(self) -> bool:
        return self.lock_state == LockState.UNAVAILABLE

    def is_thread_at_front(self, wait_number: int) -> bool:
        return len(self.wait_queue) > 0 and self.wait_queue[0] == wait_number


    def acquire(self) -> None:
        with self.condition:
            wait_number: int = self.get_next_queue_number()
            self.wait_queue.append(wait_number)
            thread_name: str = threading.current_thread().name
            logging.debug(f"Thread {thread_name} requesting the lock with wait number {wait_number}.")
            while self.is_locked() or not self.is_thread_at_front(wait_number):
                self.condition.wait()
            self.wait_queue.pop(0)
            self.lock()
            logging.debug(f"Thread {thread_name} acquired the lock.")


    def release(self) -> None:
        with self.condition:
            self.unlock()
            logging.debug(f"Thread {threading.current_thread().name} released the lock.")
            self.condition.notify_all()

    def is_available(self) -> bool:
        return self.lock_state == LockState.AVAILABLE


    def __enter__(self):
        self.acquire()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.release()
