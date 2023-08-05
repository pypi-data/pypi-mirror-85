from simses.config.data.data_config import DataConfig
from simses.constants_simses import ROOT_PATH


class TemperatureDataConfig(DataConfig):

    def __init__(self, path: str = None):
        super().__init__(path)
        self.__section: str = 'TEMPERATURE_DATA'

    @property
    def location_data_dir(self) -> str:
        """Returns directory of location data directory"""
        return ROOT_PATH + self.get_property(self.__section, 'LOCATION_DIR')

    @property
    def location_file(self) -> str:
        """Returns directory of location data file"""
        return self.location_data_dir + self.get_property(self.__section, 'LOCATION_FILE')
