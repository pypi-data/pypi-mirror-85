from simses.config.simulation.energy_management_config import EnergyManagementConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.frequency_containment_reserve import FrequencyContainmentReserve
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.intraday_market_recharge import \
    IntradayMarketRecharge
from simses.simulation.energy_management.operation_strategy.operation_priority import OperationPriority
from simses.simulation.energy_management.operation_strategy.stacked_operation_strategy.stacked_operation_strategy import \
    StackedOperationStrategy


class FcrIdmRechargeStacked(StackedOperationStrategy):

    def __init__(self, general_config: GeneralSimulationConfig, ems_config: EnergyManagementConfig,
                 profile_config: ProfileConfig):
        super().__init__(OperationPriority.VERY_HIGH, [FrequencyContainmentReserve(general_config, ems_config, profile_config),
                                                       IntradayMarketRecharge(general_config, ems_config)])
