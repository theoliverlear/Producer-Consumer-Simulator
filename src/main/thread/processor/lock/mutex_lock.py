import logging
import threading
from threading import Condition


from src.main.thread.processor.lock.lock_state import LockState


class MutexLock:
    """
    Thread-safe mutex lock implementation for synchronizing access to a shared
    resource across multiple threads.

    :ivar lock_state: The current state of the lock, indicating whether the
        lock is AVAILABLE or UNAVAILABLE.
    :type lock_state: LockState
    :ivar condition: A threading.Condition instance used for implementing
        the lock mechanism and managing thread synchronization.
    :type condition: Condition
    """
    def __init__(self):
        """
        Class to manage a thread-safe locking mechanism for resource
        availability.

        :ivar lock_state: The current state of the lock, indicating whether
        the lock is AVAILABLE or UNAVAILABLE.
        :type lock_state: LockState
        :ivar condition: A threading.Condition instance used for implementing
        the lock mechanism and managing thread synchronization.
        :type condition: Condition
        """
        self.lock_state: LockState = LockState.AVAILABLE
        self.condition: Condition = threading.Condition()

    def acquire(self) -> None:
        """
        Acquires the lock if it is not already held by another thread. If the
        lock is currently held, the method blocks the current thread until the
        lock becomes available.

        :raises threading.ThreadError: If the thread is interrupted while
        waiting to acquire the lock.

        :return: This method does not return any value.
        :rtype: None
        """
        with self.condition:
            thread_name: str = threading.current_thread().name
            while self.is_locked():
                self.condition.wait()
            self.lock()
            logging.debug(f"Thread {thread_name} acquired the lock.")

    def release(self) -> None:
        """
        Releases the lock held by the current thread and notifies all threads
        waiting for the condition.

        :return: This method does not return any value.
        :rtype: None
        """
        with self.condition:
            self.unlock()
            logging.debug(f"Thread {threading.current_thread().name} released the lock.")
            self.condition.notify_all()

    def __enter__(self):
        """
        Handles context management for acquiring and releasing resources.

        :return: The acquired resource instance.
        :rtype: object
        """
        self.acquire()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """
        Handle the cleanup and resource release when exiting a context.

        :param exception_type: The type of exception raised in the context.
        :type exception_type: type
        :param exception_value: The exception object raised in the context.
        :type exception_value: Exception
        :param exception_traceback: The traceback for the exception.
        :type exception_traceback: Traceback
        :return: This method does not return any value.
        :rtype: None
        """
        self.release()

    def is_available(self) -> bool:
        """
        Checks if the current lock state is available.

        :return: Boolean value indicating whether the lock state is set
            to AVAILABLE.
        :rtype: bool
        """
        return self.lock_state == LockState.AVAILABLE

    def lock(self) -> None:
        """
        Locks the current state by setting `lock_state` to `UNAVAILABLE`.

        :return: This method does not return any value.
        :rtype: None
        """
        self.lock_state = LockState.UNAVAILABLE

    def unlock(self) -> None:
        """
        Unlocks the current lock by changing its state to available.

        :return: This method does not return any value.
        :rtype: None
        """
        self.lock_state = LockState.AVAILABLE

    def is_locked(self) -> bool:
        """
        Determines if the lock is currently in a locked state.

        :return: Boolean indicating whether the object is in a locked state.
        :rtype: bool
        """
        return self.lock_state == LockState.UNAVAILABLE
