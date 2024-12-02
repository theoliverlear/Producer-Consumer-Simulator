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

    def simulate(self):
        self.start()
        # TODO: Add business logic
        self.stop()

    def start(self):
        pass

    def stop(self):
        pass

    def show_suggestions(self):
        pass

    def show_efficiency(self):
        pass

