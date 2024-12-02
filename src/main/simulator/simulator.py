from src.main.config.config import Config


class Simulator:
    # Thread Manager (num_producers), (num_consumers), (buffer_size)
    """
    Pipe in args
    Check validity
    Get commands
    Initialize lock
    Initialize thread manager
        - Initialize producer amount and speed
        - Initialize consumer amount and speed




    """
    def __init__(self, config: Config):
        self.config = config

    def simulate(self) -> None:
        self.start()
        # TODO: Add business logic
        self.stop()

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def show_suggestions(self) -> None:
        pass

    def show_efficiency(self) -> None:
        pass

