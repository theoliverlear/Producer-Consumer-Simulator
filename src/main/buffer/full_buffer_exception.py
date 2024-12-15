class FullBufferException(Exception):
    """
    Exception raised when attempting to fill an already full buffer.

    The FullBufferException is designed to signal that an operation has been
    attempted which would exceed the capacity of a buffer, violating
    constraints on its size.

    :ivar DEFAULT_MESSAGE: The default error message used when an instance
    of this exception is raised without a custom message.
    :type DEFAULT_MESSAGE: str
    """
    DEFAULT_MESSAGE: str = "Trying to fill an already full buffer."
    def __init__(self, message: str = DEFAULT_MESSAGE):
        super().__init__(message)