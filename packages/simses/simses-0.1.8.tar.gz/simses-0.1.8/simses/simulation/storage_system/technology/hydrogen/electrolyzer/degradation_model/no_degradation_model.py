from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.calendar_degradation.no_calendar_degradation import \
    NoCalendarDegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.cyclic_degradation.no_cyclic_degradation_model import \
    NoCyclicDegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.degradation_model import \
    DegradationModel


class NoDegradationModel(DegradationModel):

    def __init__(self):
        super().__init__(NoCyclicDegradationModel(), NoCalendarDegradationModel())

    def calculate_soh(self, state: ElectrolyzerState) -> None:
        pass

    def get_soh_el(self):
        return 1
