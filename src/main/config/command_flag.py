class CommandFlag:
    """
    Represents a command-line flag and its associated attributes.

    This class encapsulates the properties of a command-line flag, such as
    the short flag, full flag, type, default value, and help text. It is
    designed to facilitate the creation, management, and representation
    of command-line flags.

    :ivar flag: The short version of the command-line flag.
    :type flag: str
    :ivar full_flag: The full version of the command-line flag.
    :type full_flag: str
    :ivar type: The expected type of the command-line flag's value.
    :ivar default_value: The default value for this flag.
    :ivar help_text: A description of the purpose and usage of the flag.
    :type help_text: str
    """
    def __init__(self,
                 flag: str,
                 full_flag: str,
                 type,
                 default_value,
                 help_text: str):
        """
        Represents a command-line flag with its attributes such as shorthand
        flag, full-length flag, type, default value, and help text.

        :param flag: A short form used for the flag in the command-line (e.g.,
            "-h").
        :type flag: str

        :param full_flag: The full flag name used in the command-line (e.g.,
            "--help").
        :type full_flag: str
        :param type: Expected Python object type for the flag's value
            (e.g., int, str, etc.).
        :type type: Type
        :param default_value: The default value assigned to the flag when not
            specified in the command-line.
        :param help_text: Descriptive text explaining the purpose and usage of
            the flag.
        :type help_text: str
        """
        self.flag: str = flag
        self.full_flag: str = full_flag
        self.type = type
        self.default_value = default_value
        self.help_text: str = help_text

    def __str__(self):
        """
        Converts the `CommandFlag` object into its string representation,
        displaying all attributes in a formatted manner.

        :return: A string representation of the `CommandFlag` instance.
        :rtype: str
        """
        return (f'CommandFlag({self.flag}, {self.full_flag}, {self.type},'
                f' {self.default_value}, {self.help_text})')