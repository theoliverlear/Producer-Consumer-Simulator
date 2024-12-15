from enum import Enum


class ThreadState(Enum):
    """
    This class defines the possible states a thread can be in and
    is designed to provide a clear, type-safe enumeration of thread
    statuses.

    :ivar ACTIVE: Indicates that the thread is currently active.
    :type ACTIVE: str
    :ivar INACTIVE: Indicates that the thread is currently inactive.
    :type INACTIVE: str
    """
    ACTIVE: str = 'active',
    INACTIVE: str = 'inactive',