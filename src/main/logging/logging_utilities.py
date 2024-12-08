import logging


def log_in_bold(text: str) -> None:
    BOLD_ASCII: str = "\033[1m"
    log_with_modifier(text, BOLD_ASCII)

def log_with_modifier(text: str, modifier: str) -> None:
    RESET_ASCII: str = "\033[0m"
    logging.info(f"{modifier}{text}{RESET_ASCII}")

def print_logging_seperator() -> None:
    logging_seperator: str = "\n" + "-" * 60
    logging.info(logging_seperator)

def get_underline_string(text_to_underline: str) -> str:
    UNDERLINE_ASCII: str = "\033[4m"
    RESET_ASCII: str = "\033[0m"
    return f"{UNDERLINE_ASCII}{text_to_underline}{RESET_ASCII}"