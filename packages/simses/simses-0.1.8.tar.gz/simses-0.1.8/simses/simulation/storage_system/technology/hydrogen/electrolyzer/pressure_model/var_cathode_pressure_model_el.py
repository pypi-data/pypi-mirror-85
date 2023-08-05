from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.config.simulation.electrolyzer_config import ElectrolyzerConfig
from simses.simulation.storage_system.technology.hydrogen.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.ideal_var_cathode_pressure_controller import \
    IdealVarCathodePressureController
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_model import \
    PressureModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.electrolyzer_stack_model import \
    ElectrolyzerStackModel


class VarCathodePressureModel(PressureModel):

    def __init__(self, electrolyzer: ElectrolyzerStackModel, config: ElectrolyzerConfig):
        super().__init__()
        self.NOM_STACK_POWER = electrolyzer.get_nominal_stack_power()
        self.VOLUME_GAS_SEPARATOR = 0.4225 * 10 ** (-3) * self.NOM_STACK_POWER / 1000  # dm³ -> m³  0.4425 l/kW: value for Volume from H-TEC Series-ME: ME 450/1400
        self.__pressure_controller = IdealVarCathodePressureController()
        self.p_c_1 = 0  # barg
        self.p_a_1 = 0  # barg
        self.n_h2_out_c = 0  # mol  mass which is set free through the control valve at cathode side
        self.n_o2_out_a = 0  # mol  mass which is set free through the control valve at anode side
        self.pressure_cathode_desire = config.desire_pressure_cathode_el  # barg
        self.pressure_anode_desire = config.desire_pressure_anode_el  # barg
        self.h2_outflow = 0  # mol/s
        self.o2_outflow = 0  # mol/s
        self.h2o_ouflow_cathode = 0  # mol/s
        self.h2o_outflow_anode = 0  # mol/s

    def calculate(self, time, state: ElectrolyzerState):
        timestep = time - state.time
        stack_temp = state.temperature + 273.15  # °C -> K
        p_c_0 = state.pressure_cathode  # barg
        p_a_0 = state.pressure_anode  # barg
        p_h2o_0 = state.sat_pressure_h2o  # bar
        n_h2_prod = state.hydrogen_production  # mol/s at stack level
        x_h2o_c = p_h2o_0 / (1 + p_c_0 - p_h2o_0)
        n_o2_prod = state.oxygen_production  # mol/s at stack level
        x_h2o_a = p_h2o_0 / (1 + p_a_0 - p_h2o_0)
        pressure_factor_cathode = ConstantsHydrogen.IDEAL_GAS_CONST * stack_temp / self.VOLUME_GAS_SEPARATOR * \
                                  (1 + x_h2o_c) * 10 ** (-5)  # bar/mol   transfer from Pa to bar with 1bar 0 10^5 Pa = 10^5 N/m²
        self.n_h2_out_c = self.__pressure_controller.calculate_n_h2_out(p_c_0, self.pressure_cathode_desire, n_h2_prod, timestep, pressure_factor_cathode)
        self.n_o2_out_a = self.__pressure_controller.calculate_n_o2_out(p_a_0, self.pressure_cathode_desire, n_o2_prod, timestep)

        # new pressure cathode
        self.p_c_1 = p_c_0 + pressure_factor_cathode * (n_h2_prod - self.n_h2_out_c ) * timestep  # bar

        # new pressure anode
        # self.p_a_1 = p_a_0 + ConstantsHydrogen.IDEAL_GAS_CONST * stack_temp / self.VOLUME_GAS_SEPARATOR * (1 + x_h2o_a) * \
        #              (n_o2_prod - self.n_o2_out_a) * 10 ** (-5)  # bar
        self.p_a_1 = p_a_0

        # outflow rates of h2, o2 and h2o
        self.h2_outflow = self.n_h2_out_c  # mol/s
        self.o2_outflow = self.n_o2_out_a  # mol/s
        self.h2o_ouflow_cathode = x_h2o_c * self.h2_outflow  # mol/s
        self.h2o_outflow_anode = x_h2o_a * self.o2_outflow  # mol/s

    def get_pressure_cathode(self) -> float:
        return self.p_c_1

    def get_pressure_anode(self) -> float:
        return self.p_a_1

    def get_h2_outflow(self) -> float:
        return self.h2_outflow

    def get_o2_outflow(self) -> float:
        return self.o2_outflow

    def get_h2o_outflow_cathode(self) -> float:
        return self.h2o_ouflow_cathode

    def get_h2o_outflow_anode(self) -> float:
        return self.h2o_outflow_anode
