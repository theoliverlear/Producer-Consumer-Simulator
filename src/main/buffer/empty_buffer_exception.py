class EmptyBufferException(Exception):
    DEFAULT_MESSAGE: str = "Trying to empty an already empty buffer."
    def __init__(self, message: str = DEFAULT_MESSAGE):
        super().__init__(message)