from enum import Enum


class LockState(Enum):
    """
    This Enum class defines the states a lock can have, providing clear and
    standardized representations to determine whether a lock is available
    or unavailable.

    :ivar AVAILABLE: Indicates the lock is available.
    :type AVAILABLE: str
    :ivar UNAVAILABLE: Indicates the lock is unavailable.
    :type UNAVAILABLE: str
    """
    AVAILABLE: str = 'available',
    UNAVAILABLE: str = 'unavailable',