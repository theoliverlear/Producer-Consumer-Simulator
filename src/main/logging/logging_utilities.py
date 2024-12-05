import logging


def log_in_bold(text: str) -> None:
    BOLD_ASCII: str = "\033[1m"
    log_with_modifier(text, BOLD_ASCII)

def log_with_modifier(text: str, modifier: str) -> None:
    RESET_ASCII: str = "\033[0m"
    logging.info(f"{modifier}{text}{RESET_ASCII}")