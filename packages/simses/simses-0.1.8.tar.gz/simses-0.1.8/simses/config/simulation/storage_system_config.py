from configparser import ConfigParser

from simses.config.simulation.simulation_config import SimulationConfig, create_dict_from, create_list_from, clean_split


class StorageSystemConfig(SimulationConfig):
    """
    Storage system specific configs
    """

    AC_SYSTEM_NAME: int = 0
    AC_SYSTEM_POWER: int = 1
    AC_SYSTEM_DC_VOLTAGE: int = 2
    AC_SYSTEM_CONVERTER: int = 3
    AC_SYSTEM_THERMAL_MODEL: int = 4
    AC_SYSTEM_HOUSING: int = 5
    AC_SYSTEM_HVAC: int = 6

    DC_SYSTEM_NAME: int = 0
    DC_SYSTEM_CONVERTER: int = 1
    DC_SYSTEM_STORAGE: int = 2

    ACDC_CONVERTER_TYPE: int = 0
    ACDC_CONVERTER_NUMBERS: int = 1

    DCDC_CONVERTER_TYPE: int = 0
    DCDC_CONVERTER_POWER: int = 1

    HVAC_TYPE: int = 0
    HVAC_POWER: int = 1
    HVAC_TEMPERATURE_SETPOINT: int = 2

    AMBIENT_TEMPERATURE_MODEL: int = 0
    AMBIENT_TEMPERATURE_CONSTANT: int = 1

    STORAGE_CAPACITY: int = 0
    STORAGE_TECHNOLOGY: int = 1

    BATTERY_CELL: int = 2
    BATTERY_SOH: int = 3

    REDOX_FLOW_STACK: int = 2
    STACK_MODULE_POWER: int = 3
    REDOX_FLOW_PUMP_ALGORITHM: int = 4

    FUEL_CELL_TYPE: int = 2
    FUEL_CELL_POWER: int = 3
    ELECTROLYZER_TYPE: int = 4
    ELECTROLYZER_POWER: int = 5
    HYDROGEN_STORAGE: int = 6
    HYDROGEN_TANK_PRESSURE: int = 7

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        self.__section: str = 'STORAGE_SYSTEM'

    @property
    def storage_systems_dc(self) -> [[str]]:
        """Returns a list of dc storage systems"""
        props: [str] = clean_split(self.get_property(self.__section, 'STORAGE_SYSTEM_DC'))
        return create_list_from(props)

    @property
    def storage_systems_ac(self) -> [[str]]:
        """Returns a list of ac storage systems"""
        props: [str] = clean_split(self.get_property(self.__section, 'STORAGE_SYSTEM_AC'))
        return create_list_from(props)

    @property
    def acdc_converter(self) -> dict:
        """Returns a list of acdc converter"""
        props: [str] = clean_split(self.get_property(self.__section, 'ACDC_CONVERTER'))
        return create_dict_from(props)

    @property
    def dcdc_converter(self) -> dict:
        """Returns a list of acdc converter"""
        props: [str] = clean_split(self.get_property(self.__section, 'DCDC_CONVERTER'))
        return create_dict_from(props)

    @property
    def hvac(self) -> dict:
        """Returns a list of hvac systems"""
        props: [str] = clean_split(self.get_property(self.__section, 'HVAC'))
        return create_dict_from(props)

    @property
    def storage_technologies(self) -> dict:
        """Returns a list of storage technologies"""
        props: [str] = clean_split(self.get_property(self.__section, 'STORAGE_TECHNOLOGY'))
        return create_dict_from(props)

    @property
    def ambient_temperature_model(self) -> list:
        """Returns name of ambient temperature model"""
        props: [str] = clean_split(self.get_property(self.__section, 'AMBIENT_TEMPERATURE_MODEL'), ',')
        return props

    @property
    def cycle_detector(self) -> str:
        """Returns name of cycle detector"""
        return self.get_property(self.__section, 'CYCLE_DETECTOR')

    @property
    def power_distributor_dc(self) -> str:
        """Returns name of cycle detector"""
        return self.get_property(self.__section, 'POWER_DISTRIBUTOR_DC')

    @property
    def power_distributor_ac(self) -> str:
        """Returns name of cycle detector"""
        return self.get_property(self.__section, 'POWER_DISTRIBUTOR_AC')
