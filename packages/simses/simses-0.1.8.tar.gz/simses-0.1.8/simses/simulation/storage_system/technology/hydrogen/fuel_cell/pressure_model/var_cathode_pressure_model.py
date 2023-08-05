from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.simulation.storage_system.technology.hydrogen.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_controller import \
    PressureController
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_model import \
    PressureModel


class VarCathodePressureModel(PressureModel):

    def __init__(self, pressure_controller: PressureController):
        super().__init__()
        self.__pressure_controller = pressure_controller
        self.volume_gas_separator = 500 / (100 * 100)  # cm² -> m²
        self.p_c_1 = 0  # barg
        self.p_a_1 = 0  # barg
        self.n_h2_out_c = 0  # mol  mass which is set free through the control valve at cathode side
        self.n_o2_out_a = 0  # mol  mass which is set free through the control valve at anode side
        self.pressure_cathode_desire = 20  # barg
        self.pressure_anode_desire = 0  # barg
        self.h2_outflow = 0  # mol/s
        self.o2_outflow = 0  # mol/s

    def calculate(self, time, state: ElectrolyzerState):
        delta_time = time - state.time
        stack_temp = state.temperature  #  K
        p_c_0 = state.pressure_cathode  # barg
        p_a_0 = state.pressure_anode  # barg
        p_h2o_0 = state.sat_pressure_h2o  # bar
        n_h2_prod = state.hydrogen_production * delta_time  # mol
        x_h2o_c = p_h2o_0 / (p_c_0 - p_h2o_0)
        n_o2_prod = state.oxygen_production * delta_time
        x_h2o_a = p_h2o_0 / (p_a_0 - p_h2o_0)
        self.n_h2_out_c = self.__pressure_controller.calculate_n_h2_out(p_c_0, self.pressure_cathode_desire, n_h2_prod)
        self.n_o2_out_a = self.__pressure_controller.calculate_n_o2_out(p_a_0, self.pressure_cathode_desire, n_o2_prod)

        # new pressure cathode
        self.p_c_1 = p_c_0 + ConstantsHydrogen.IDEAL_GAS_CONST * stack_temp / self.volume_gas_separator * (1 + x_h2o_c) * \
                     (n_h2_prod - self.n_h2_out_c ) * 10 ** (-5)  # bar

        # new pressure anode
        self.p_a_1 = p_a_0 + ConstantsHydrogen.IDEAL_GAS_CONST * stack_temp / self.volume_gas_separator * (1 + x_h2o_a) * \
                     (n_o2_prod - self.n_o2_out_a) * 10 ** (-5)  # bar

        # outflow rates of h2 and o2
        self.h2_outflow = self.n_h2_out_c / delta_time
        self.o2_outflow = self.n_o2_out_a / delta_time

    def get_pressure_cathode(self) -> float:
        return self.p_c_1

    def get_pressure_anode(self) -> float:
        return self.p_a_1

    def get_h2_outflow(self) -> float:
        return self.h2_outflow

    def get_o2_outflow(self) -> float:
        return self.o2_outflow
