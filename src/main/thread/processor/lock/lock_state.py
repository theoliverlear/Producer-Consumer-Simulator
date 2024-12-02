from enum import Enum


class LockState(Enum):
    AVAILABLE = 'available',
    UNAVAILABLE = 'unavailable',