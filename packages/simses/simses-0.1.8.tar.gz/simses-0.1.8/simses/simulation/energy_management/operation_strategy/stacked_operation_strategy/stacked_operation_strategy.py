from simses.commons.state.energy_management_state import EnergyManagementState
from simses.commons.state.system_state import SystemState
from simses.simulation.energy_management.operation_strategy.operation_strategy import OperationStrategy


class StackedOperationStrategy(OperationStrategy):
    """
    Algorithm to determine output power for each operation (in multiuse case) of the ESS for the next timestep.
    """

    def __init__(self, priority: float, strategies: []):
        super().__init__(priority)
        OperationStrategy.sort(strategies)
        self.__strategies: [] = strategies

    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        for strategy in self.__strategies:
            power += strategy.next(time, system_state, power)
        return power

    def update(self, energy_management_state: EnergyManagementState) -> None:
        for strategy in self.__strategies:
            strategy.update(energy_management_state)

    def clear(self) -> None:
        for strategy in self.__strategies:
            strategy.clear()

    def close(self) -> None:
        for strategy in self.__strategies:
            strategy.close()
