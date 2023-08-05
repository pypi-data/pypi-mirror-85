from simses.config.config import Config


class DataConfig(Config):

    """
    DataConfig objects provide information for each specific system path to data
    """

    config_name: str = 'data'

    def __init__(self, path: str):
        super().__init__(path, self.config_name, None)
