import logging
from configparser import ConfigParser

from simses.config.config import Config


class LogConfig(Config):

    config_name: str = 'logger'
    __config_parser: ConfigParser = None

    def __init__(self, path: str = None):
        super().__init__(path, self.config_name, self.__config_parser)
        self.__section: str = 'LOGGING'

    @classmethod
    def set_config(cls, config: ConfigParser) -> None:
        cls.__config_parser = config

    @property
    def log_level(self) -> int:
        """Returns log level"""
        try:
            level: str = self.get_property(self.__section, 'LOG_LEVEL')
            if level == 'DEBUG':
                return logging.DEBUG
            elif level == 'INFO':
                return logging.INFO
            elif level == 'WARNING':
                return logging.WARNING
            elif level == 'ERROR':
                return logging.ERROR
            else:
                return logging.DEBUG
        except:
            return logging.ERROR

    @property
    def log_to_console(self) -> bool:
        return self.get_property(self.__section, 'LOG_TO_CONSOLE') in ['True']

    @property
    def log_to_file(self) -> bool:
        return self.get_property(self.__section, 'LOG_TO_FILE') in ['True']
