class FullBufferException(Exception):
    DEFAULT_MESSAGE: str = "Trying to fill an already full buffer."
    def __init__(self, message: str = DEFAULT_MESSAGE):
        super().__init__(message)