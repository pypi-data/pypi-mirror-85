from configparser import ConfigParser

from simses.config.simulation.simulation_config import SimulationConfig


class ElectrolyzerConfig(SimulationConfig):
    """
    Electrolyzer specific configs
    """

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        self.__section: str = 'ELECTROLYZER'

    @property
    def eol_electrolyzer(self) -> float:
        """Returns end of life criterion from data_config file_name"""
        return float(self.get_property(self.__section, 'EOL'))

    @property
    def desire_pressure_cathode_el(self) -> float:
        """Retruns desired pressure of cathode of electrolyzer"""
        return float(self.get_property(self.__section, 'PRESSURE_CATHODE'))

    @property
    def desire_pressure_anode_el(self) -> float:
        """Retruns desired pressure of cathode of electrolyzer"""
        return float(self.get_property(self.__section, 'PRESSURE_ANODE'))

    @property
    def desire_temperature_el(self) -> float:
        """Retruns desired pressure of cathode of electrolyzer"""
        return float(self.get_property(self.__section, 'TEMPERATURE'))

    @property
    def total_pressure(self) -> float:
        """Retruns desired pressure of cathode of electrolyzer"""
        return float(self.get_property(self.__section, 'TOTAL_PRESSURE'))
