import pandas as pd
import scipy.interpolate
from math import log10

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.config.data.redox_flow_data_config import RedoxFlowDataConfig
from simses.config.simulation.redox_flow_config import RedoxFlowConfig
from simses.simulation.storage_system.technology.redox_flow.stack_module.electrolyte_system.electrolyte_system import \
    ElectrolyteSystem
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class CellDataStack5600W(StackModule):
    """A stack is part of a stack module, Stacks can be connected serial of parallel to a stack module."""

    __STACK_POWER_NOM = 5600  # W
    __CELL_NUMBER = 40  # -
    __CELL_AREA = 2160  # cm^2
    __ELECTRODE_THICKNESS = 0.37  # cm
    __ELECTRODE_POROSITY = 0.9  # -
    __MIN_CELL_VOLTAGE = 1.0  # V
    __MAX_CELL_VOLTAGE = 1.6  # V
    __SELF_DISCHARGE_CURRENT_DENS = 1  # mA/cm^2
    __HYDRAULIC_RESISTANCE = 2.84e10  # 1/m^3

    __SOC_IDX = 0
    __TEMP_IDX = 1
    __2D_RINT = False  # True if temperature dependency should be considered in internal resistance.

    def __init__(self, electrolyte_system: ElectrolyteSystem, voltage: float, power: float,
                 redox_flow_data_config: RedoxFlowDataConfig, redox_flow_config: RedoxFlowConfig):
        super().__init__(electrolyte_system, voltage, power, self.__CELL_NUMBER, self.__STACK_POWER_NOM,
                         redox_flow_config)
        self.__log: Logger = Logger(__name__)
        self.__electrolyte_system: ElectrolyteSystem = electrolyte_system
        self.__RINT_FILE = redox_flow_data_config.rfb_rint_file
        pd.set_option('precision', 9)
        self.__internal_resistance = pd.read_csv(self.__RINT_FILE, delimiter=';', decimal=",")  # Ohm
        self.__soc_arr = self.__internal_resistance.iloc[:, self.__SOC_IDX]
        self.__temp_arr = self.__internal_resistance.iloc[:3, self.__TEMP_IDX]
        if self.__2D_RINT:
            self.__rint_mat_ch = self.__internal_resistance.iloc[:, 2:5]
            self.__rint_mat_dch = self.__internal_resistance.iloc[:, 5:]
            self.__rint_ch_inter2d = scipy.interpolate.interp2d(self.__temp_arr, self.__soc_arr, self.__rint_mat_ch,
                                                                kind='linear', fill_value=None)
            self.__rint_dis_inter2d = scipy.interpolate.interp2d(self.__temp_arr, self.__soc_arr, self.__rint_mat_dch,
                                                                 kind='linear', fill_value=None)
        else:
            self.__rint_mat_ch = self.__internal_resistance.iloc[:, 4]
            self.__rint_mat_dch = self.__internal_resistance.iloc[:, 7]
            self.__rint_ch_inter1d = scipy.interpolate.interp1d(self.__soc_arr, self.__rint_mat_ch, kind='linear',
                                                                fill_value='extrapolate')
            self.__rint_dis_inter1d = scipy.interpolate.interp1d(self.__soc_arr, self.__rint_mat_dch, kind='linear',
                                                                 fill_value='extrapolate')
        self.__temperature = 303.15  # K

    def get_open_circuit_voltage(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Literature source: Fink, Holger. Untersuchung von Verlustmechanismen in Vanadium-Flussbatterien. Diss.
        Technische Universität München, 2019.
        equation 5.18, assumption: SOH = 100 %, therefore ver = 0.5
        """
        concentration_v = self.__electrolyte_system.get_vanadium_concentration()
        soc_stack = redox_flow_state.soc_stack
        temperature = redox_flow_state.electrolyte_temperature
        concentration_h_start = 2.6  # mol/l
        ocv_cell = (1.255 + 0.07 + 0.059 * temperature / 298.15 * log10((soc_stack / (1 - soc_stack) *
                    (concentration_h_start + concentration_v / 1000 * (soc_stack + 0.5)))**2 * (concentration_h_start +
                    concentration_v / 1000 * (soc_stack - 0.5))))
        self.__log.debug('OCV_cell: ' + str(ocv_cell) + ' V')
        return ocv_cell * self.get_cell_per_stack() * self.get_serial_scale()

    def get_nominal_voltage_cell(self) -> float:
        """Calculated for a temperature of 30 °C and at SOC 50 %."""
        nominal_voltage_cell = 1.425
        return nominal_voltage_cell

    def get_internal_resistance(self, redox_flow_state: RedoxFlowState) -> float:
        soc = redox_flow_state.soc
        temp = self.__temperature
        if redox_flow_state.is_charge:
            # internal resistance for charging
            if self.__2D_RINT:
                resistance = self.__rint_ch_inter2d(temp, soc)
            else:
                resistance = self.__rint_ch_inter1d(soc)
            self.__log.debug('Resistance charging stack: ' + str(resistance) + ' Ohm, resistance charging module:'
                             + str(resistance / self.get_parallel_scale() * self.get_serial_scale()))
            return float(resistance / self.get_parallel_scale() * self.get_serial_scale())
        else:
            # internal resistance for discharging
            if self.__2D_RINT:
                resistance = self.__rint_dis_inter2d(temp, soc)
            else:
                resistance = self.__rint_dis_inter1d(soc)
            self.__log.debug('Resistance discharging stack: ' + str(resistance) + ' Ohm, resistance discharging module:'
                             + str(resistance / self.get_parallel_scale() * self.get_serial_scale()))
            return float(resistance / self.get_parallel_scale() * self.get_serial_scale())

    def get_cell_per_stack(self) -> int:
        return self.__CELL_NUMBER

    def get_min_voltage(self) -> float:
        return self.__MIN_CELL_VOLTAGE * self.get_cell_per_stack() * self.get_serial_scale()

    def get_max_voltage(self) -> float:
        return self.__MAX_CELL_VOLTAGE * self.get_cell_per_stack() * self.get_serial_scale()

    def get_self_discharge_current(self, redox_flow_state: RedoxFlowState) -> float:
        return (self.__SELF_DISCHARGE_CURRENT_DENS / 1000 * self.get_specif_cell_area() * self.get_cell_per_stack() *
                self.get_serial_scale() * self.get_parallel_scale())

    def get_stacks_volume(self) -> float:
        stack_electrolyte_volume = (self.get_specif_cell_area() * self.__ELECTRODE_THICKNESS / 1000000 *
                                    self.__ELECTRODE_POROSITY * self.get_cell_per_stack() * self.get_serial_scale() *
                                    self.get_parallel_scale())
        if self.get_total_electrolyte_volume() < stack_electrolyte_volume:
            return self.get_total_electrolyte_volume()
        else:
            return stack_electrolyte_volume

    def get_electrolyte_temperature(self) -> float:
        return self.__temperature

    def get_specif_cell_area(self) -> float:
        return self.__CELL_AREA

    def get_hydraulic_resistance(self) -> float:
        return self.__HYDRAULIC_RESISTANCE / (self.get_serial_scale() * self.get_parallel_scale())

    def close(self):
        super().close()
        self.__log.close()
        self.__electrolyte_system.close()
