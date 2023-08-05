import pandas

from simses.analysis.data.data import Data
from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.config.simulation.general_config import GeneralSimulationConfig


class LithiumIonData(Data):
    """
    Provides time series data from LithiumIonState
    """

    def __init__(self, config: GeneralSimulationConfig, data: pandas.DataFrame):
        super().__init__(config, data)

    @property
    def id(self) -> str:
        return str(int(self._get_first_value(LithiumIonState.SYSTEM_AC_ID))) + '.' + \
               str(int(self._get_first_value(LithiumIonState.SYSTEM_DC_ID)))

    @property
    def time(self):
        return self._get_data(LithiumIonState.TIME)

    @property
    def power(self):
        return self._get_data(LithiumIonState.VOLTAGE) * self._get_data(LithiumIonState.CURRENT)

    @property
    def dc_power(self):
        return self.power

    @property
    def energy_difference(self):
        soc = self._get_difference(LithiumIonState.SOC)
        capacity = self.initial_capacity
        return soc * capacity

    @property
    def soc(self):
        return self._get_data(LithiumIonState.SOC)

    @property
    def capacity(self):
        return self._get_data(LithiumIonState.CAPACITY) / 1000.0

    @property
    def state_of_health(self):
        return self._get_data(LithiumIonState.SOH)

    @property
    def resistance(self):
        return self._get_data(LithiumIonState.INTERNAL_RESISTANCE)

    @property
    def resistance_increase(self):
        return self._get_data(LithiumIonState.RESISTANCE_INCREASE)

    @property
    def storage_fulfillment(self):
        return self._get_data(LithiumIonState.FULFILLMENT)

    @property
    def temperature(self):
        return self._get_data(LithiumIonState.TEMPERATURE)

    @classmethod
    def get_system_data(cls, path: str, config: GeneralSimulationConfig) -> list:
        system_data: [pandas.DataFrame] = cls._get_system_data_for(path, LithiumIonState, LithiumIonState.TIME,
                                                                   LithiumIonState.SYSTEM_AC_ID, LithiumIonState.SYSTEM_DC_ID)
        res: [LithiumIonData] = list()
        for data in system_data:
            res.append(LithiumIonData(config, data))
        return res


