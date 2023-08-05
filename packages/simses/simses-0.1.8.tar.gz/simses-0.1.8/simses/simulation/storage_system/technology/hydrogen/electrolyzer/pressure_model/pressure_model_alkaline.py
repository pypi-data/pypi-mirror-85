from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.no_pressure_controller import \
    NoPressureController
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_model import \
    PressureModel


class AlkalinePressureModel(PressureModel):

    def __init__(self):
        super().__init__()
        self.__pressure_cathode_el = 0  # barg
        self.__pressure_anode_el = 0  # barg
        self.__pressure_cathode_desire_el = 0  # barg
        self.__pressure_anode_desire_el = 0  # barg
        self.__hydrogen_outflow = 0  # mol/s
        self.__oxygen_outflow = 0  # mol/s
        self.pressure_controller = NoPressureController()

    def calculate(self, time, state: ElectrolyzerState) -> None:
        # Express anode/cathode pressure relative to atmospheric pressure, for implementation with existing hydrogen storage model
        self.__pressure_anode_el = state.total_pressure - 1     # in barg
        self.__pressure_cathode_el = state.total_pressure - 1   # in barg
        hydrogen_produced = state.hydrogen_production
        oxygen_produced = state.oxygen_production
        self.__hydrogen_outflow = self.pressure_controller.calculate_n_h2_out(self.__pressure_cathode_el, self.__pressure_cathode_desire_el, hydrogen_produced, 0)
        self.__oxygen_outflow = self.pressure_controller.calculate_n_o2_out(self.__pressure_anode_el, self.__pressure_anode_desire_el, oxygen_produced)

    def get_pressure_anode(self) -> float:
        return self.__pressure_anode_el

    def get_pressure_cathode(self) -> float:
        return self.__pressure_cathode_el

    def get_h2_outflow(self) -> float:
        return self.__hydrogen_outflow

    def get_o2_outflow(self) -> float:
        return self.__oxygen_outflow

    def get_h2o_outflow_cathode(self) -> float:
        return 0

    def get_h2o_outflow_anode(self) -> float:
        return 0
