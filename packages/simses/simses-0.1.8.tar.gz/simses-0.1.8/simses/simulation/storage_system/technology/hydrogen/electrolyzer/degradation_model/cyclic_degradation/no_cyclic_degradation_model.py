from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.cyclic_degradation.cyclic_degradation_model import \
    CyclicDegradationModel


class NoCyclicDegradationModel(CyclicDegradationModel):

    def __init__(self):
        super().__init__()

    def calculate_resistance_increase(self, time: float, state: ElectrolyzerState) -> None:
        pass

    def calculate_exchange_current_dens_decrerase(self, state: ElectrolyzerState):
        pass

    def get_resistance_increase(self) -> float:
        return 0

    def get_exchange_current_dens_decrease(self) -> float:
        return 0

    def reset(self, hydrogen_state: ElectrolyzerState) -> None:
        pass

    def close(self) -> None:
        pass