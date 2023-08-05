from datetime import datetime

from simses.commons.profile.power_profile.power_profile import PowerProfile
from simses.commons.state.energy_management_state import EnergyManagementState
from simses.commons.state.system_state import SystemState
from simses.config.simulation.energy_management_config import EnergyManagementConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.peak_shaving_simple import \
    SimplePeakShaving
from simses.simulation.energy_management.operation_strategy.operation_priority import OperationPriority
from simses.simulation.energy_management.operation_strategy.operation_strategy import OperationStrategy
from simses.simulation.energy_management.operation_strategy.stacked_operation_strategy.fcr_idm_recharge_stacked import \
    FcrIdmRechargeStacked


class FcrIdmPeakShavingSerial(OperationStrategy):

    __FCR_START = 8  # h
    __FCR_STOP = 15  # h

    def __init__(self, general_config: GeneralSimulationConfig, ems_config: EnergyManagementConfig,
                 profile_config: ProfileConfig, power_profile: PowerProfile):
        super().__init__(OperationPriority.VERY_HIGH)
        self.__fcr_idm_strategy: OperationStrategy = FcrIdmRechargeStacked(general_config, ems_config, profile_config)
        self.__peak_shaving_strategy: OperationStrategy = SimplePeakShaving(power_profile, ems_config)
        self.__strategies: [OperationStrategy] = list()
        self.__strategies.append(self.__fcr_idm_strategy)
        self.__strategies.append(self.__peak_shaving_strategy)

    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        tstmp = datetime.utcfromtimestamp(time)
        hour = tstmp.hour + tstmp.minute / 60. + tstmp.second / 3600.
        power_peak_shaving = self.__peak_shaving_strategy.next(time, system_state, power)
        power_fcr = self.__fcr_idm_strategy.next(time, system_state, power)
        if self.__FCR_START <= hour < self.__FCR_STOP:
            self.__peak_shaving_strategy.clear()
            return power_fcr
        else:
            self.__fcr_idm_strategy.clear()
            return power_peak_shaving

    def update(self, energy_management_state: EnergyManagementState) -> None:
        for strategy in self.__strategies:
            strategy.update(energy_management_state)

    def clear(self) -> None:
        for strategy in self.__strategies:
            strategy.clear()

    def close(self) -> None:
        for strategy in self.__strategies:
            strategy.close()
