import logging


def log_in_bold(text: str) -> None:
    """
    Logs a given text in bold formatting by applying an ASCII bold modifier.

    :param text: The text string to be logged in bold formatting.
    :type text: str
    :return: None
    """
    BOLD_ASCII: str = "\033[1m"
    log_with_modifier(text, BOLD_ASCII)

def log_with_modifier(text: str, modifier: str) -> None:
    """
    Logs a given text message with a specified modifier, such as color, style,
    or decoration, using an ASCII escape sequence.

    :param text: The text message to be logged.
    :type text: str
    :param modifier: The ASCII modifier to apply to text (e.g., color codes).
    :type modifier: str
    :return: This function does not return a value.
    :rtype: None
    """
    RESET_ASCII: str = "\033[0m"
    logging.info(f"{modifier}{text}{RESET_ASCII}")

def print_logging_seperator() -> None:
    """
    Prints a logging separator line to visually differentiate log sections.

    :rtype: None
    :return: None
    """
    logging_seperator: str = "\n" + "-" * 60
    logging.info(logging_seperator)

def get_underline_string(text_to_underline: str) -> str:
    """
    Generates and returns a string with the given text underlined using
    ANSI escape sequences.

    :param text_to_underline: A string to be formatted with an underline.
    :return: A string formatted with underline ANSI escape sequences.
    :rtype: str
    """
    UNDERLINE_ASCII: str = "\033[4m"
    RESET_ASCII: str = "\033[0m"
    return f"{UNDERLINE_ASCII}{text_to_underline}{RESET_ASCII}"