import logging
import threading
from threading import Condition


from src.main.thread.processor.lock.lock_state import LockState


class MutexLock:
    def __init__(self):
        self.lock_state: LockState = LockState.AVAILABLE
        self.condition: Condition = threading.Condition()

    def acquire(self) -> None:
        with self.condition:
            thread_name: str = threading.current_thread().name
            while self.is_locked():
                self.condition.wait()
            self.lock()
            logging.debug(f"Thread {thread_name} acquired the lock.")

    def release(self) -> None:
        with self.condition:
            self.unlock()
            logging.debug(f"Thread {threading.current_thread().name} released the lock.")
            self.condition.notify_all()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.release()

    def is_available(self) -> bool:
        return self.lock_state == LockState.AVAILABLE

    def lock(self):
        self.lock_state = LockState.UNAVAILABLE

    def unlock(self):
        self.lock_state = LockState.AVAILABLE

    def is_locked(self) -> bool:
        return self.lock_state == LockState.UNAVAILABLE
