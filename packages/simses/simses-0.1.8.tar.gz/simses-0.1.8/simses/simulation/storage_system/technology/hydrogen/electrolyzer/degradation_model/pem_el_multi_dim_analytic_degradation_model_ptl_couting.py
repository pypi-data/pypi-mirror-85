from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.config.simulation.electrolyzer_config import ElectrolyzerConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.calendar_degradation.calendar_degradation_pem_el_multi_dim_analytic import \
    CalendarDegradationPemElMultiDimAnalyitic
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.cyclic_degradation.cyclic_degradation_pem_el_multi_dim_analyitc_ptl_coating import \
    CyclicDegradationPemElMultiDimAnalyticPtlCoating
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.degradation_model import \
    DegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.electrolyzer_stack_model import \
    ElectrolyzerStackModel


class PemElMultiDimAnalyticDegradationModelPtlCoating(DegradationModel):

    def __init__(self, electrolyzer: ElectrolyzerStackModel, config: ElectrolyzerConfig,
                 general_config: GeneralSimulationConfig):
        super().__init__(CyclicDegradationPemElMultiDimAnalyticPtlCoating(),
                         CalendarDegradationPemElMultiDimAnalyitic(general_config))

        self.__end_of_life = config.eol_electrolyzer
        self.__rev_voltage_bol = electrolyzer.get_reference_voltage_eol(0, 1)
        self.__voltage_increase_eol = 0.27  # V
        self.__soh = 1  # p.u.

    def calculate_soh(self, state: ElectrolyzerState) -> None:
        self.__soh = 1 - 0.2 * (state.reference_voltage - self.__rev_voltage_bol) / \
                     self.__voltage_increase_eol

    def get_soh_el(self):
        return self.__soh