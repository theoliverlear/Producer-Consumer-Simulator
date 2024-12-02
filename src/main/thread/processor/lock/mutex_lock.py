import threading

from src.main.thread.processor.lock.lock_state import LockState


class MutexLock:
    def __init__(self):
        self.lock_state: LockState = LockState.AVAILABLE
        self.lock: threading.Lock = threading.Lock()

    def acquire(self):
        self.lock.acquire()
        self.lock_state = LockState.UNAVAILABLE

    def release(self):
        self.lock_state = LockState.AVAILABLE
        self.lock.release()

    def is_available(self):
        return self.lock_state == LockState.AVAILABLE


    def __enter__(self):
        self.acquire()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.release()
