class EmptyBufferException(Exception):
    """
    Exception raised when attempting to empty an already empty buffer.

    This exception is used to indicate that an operation which tries to
    remove elements from a buffer has been performed, but the buffer
    was already empty.

    :ivar DEFAULT_MESSAGE: Default error message used when the exception
        is raised without a custom message.
    :type DEFAULT_MESSAGE: str
    """
    DEFAULT_MESSAGE: str = "Trying to empty an already empty buffer."
    def __init__(self, message: str = DEFAULT_MESSAGE):
        super().__init__(message)