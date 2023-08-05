from configparser import ConfigParser
from datetime import datetime

from pytz import timezone

from simses.config.simulation.simulation_config import SimulationConfig


class GeneralSimulationConfig(SimulationConfig):
    """
    General simulation configs
    """

    __UTC: timezone = timezone('UTC')

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        self.__section: str = 'GENERAL'

    @property
    def timestep(self) -> float:
        """Returns simulation timestep in s"""
        return float(self.get_property(self.__section, 'TIME_STEP'))

    @property
    def start(self) -> float:
        """Returns simulation start timestamp"""
        date: str = self.get_property(self.__section, 'START')
        return self.__extract_utc_timestamp_from(date)

    @property
    def end(self) -> float:
        """Returns simulation end timestamp"""
        date: str = self.get_property(self.__section, 'END')
        return self.__extract_utc_timestamp_from(date)

    def __extract_utc_timestamp_from(self, date: str) -> float:
        date: datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return self.__UTC.localize(date).timestamp()

    @property
    def duration(self) -> float:
        """Returns simulation duration in s from __analysis_config file_name"""
        return self.end - self.start

    @property
    def loop(self) -> int:
        """Returns number of simulation loops"""
        return int(self.get_property(self.__section, 'LOOP'))

    @property
    def export_interval(self) -> float:
        """Returns interval to write value to file"""
        return float(self.get_property(self.__section, 'EXPORT_INTERVAL'))

    @property
    def export_data(self) -> bool:
        """Returns selection for data export True/False"""
        return self.get_property(self.__section, 'EXPORT_DATA') in ['True']