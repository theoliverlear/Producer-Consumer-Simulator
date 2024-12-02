class CommandFlag:
    def __init__(self, flag: str, full_flag: str, value: str):
        self.flag: str = flag
        self.full_flag: str = full_flag
        self.value: str = value