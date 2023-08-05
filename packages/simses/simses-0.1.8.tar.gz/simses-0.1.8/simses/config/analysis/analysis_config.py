from configparser import ConfigParser

from simses.config.config import Config


class AnalysisConfig(Config):
    """
    All analysis configs are inherited from this class
    """

    config_name: str = 'analysis'

    def __init__(self, path: str, config: ConfigParser):
        super().__init__(path, self.config_name, config)
