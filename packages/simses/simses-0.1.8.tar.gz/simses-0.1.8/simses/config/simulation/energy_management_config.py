from configparser import ConfigParser

from simses.config.simulation.simulation_config import SimulationConfig


class EnergyManagementConfig(SimulationConfig):
    """
    Energy management specific configs
    """

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        self.__section: str = 'ENERGY_MANAGEMENT'

    @property
    def operation_strategy(self) -> str:
        """Returns operation strategy from __analysis_config file_name"""
        return self.get_property(self.__section, 'STRATEGY')

    @property
    def max_fcr_power(self) -> float:
        """Returns max power for providing frequency containment reserve from __analysis_config file_name"""
        return float(self.get_property(self.__section, 'POWER_FCR'))

    @property
    def max_idm_power(self) -> float:
        """Returns max power for intra day market transactions from __analysis_config file_name"""
        return float(self.get_property(self.__section, 'POWER_IDM'))

    @property
    def soc_set(self) -> float:
        """Returns the optimal soc for a FCR storage from __analysis_config file_name.
        In case of an overall efficiency below 1, the optimal soc should be higher than 0.5"""
        return float(self.get_property(self.__section, 'SOC_SET'))

    @property
    def max_power(self) -> float:
        """Returns max power for peak shaving from __analysis_config file_name"""
        return float(self.get_property(self.__section, 'MAX_POWER'))

    @property
    def min_soc(self) -> float:
        """Returns min soc from __analysis_config file_name"""
        return float(self.get_property(self.__section, 'MIN_SOC'))

    @property
    def max_soc(self) -> float:
        """Returns max soc from __analysis_config file_name"""
        return float(self.get_property(self.__section, 'MAX_SOC'))
