class CommandFlag:
    def __init__(self, flag: str, full_flag: str, type, default_value, help_text: str):
        self.flag = flag
        self.full_flag = full_flag
        self.type = type
        self.default_value = default_value
        self.help_text = help_text

    def __str__(self):
        return f'CommandFlag({self.flag}, {self.full_flag}, {self.type}, {self.default_value}, {self.help_text})'