import numpy as np

from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.config.simulation.electrolyzer_config import ElectrolyzerConfig
from simses.simulation.storage_system.auxiliary.pump.pump import Pump
from simses.simulation.storage_system.auxiliary.water_heating.water_heating import WaterHeating
from simses.simulation.storage_system.technology.hydrogen.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.electrolyzer_stack_model import \
    ElectrolyzerStackModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.ideal_var_flow_thermal_controller import \
    IdealVarFlowThermalController
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_model import \
    ThermalModel
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class SimpleThermalModelAlkaline(ThermalModel):
    """ This model functions at Electrolyzer Level.
    This model calculates the temperaturechange in the electrlyzer stack
    the elelctrolyzer is represented by a area element"""

    def __init__(self, electrolyzer: ElectrolyzerStackModel, water_heating: WaterHeating, pump: Pump,
                 ambient_thermal_model: AmbientThermalModel, config: ElectrolyzerConfig):
        super().__init__()
        self.__ambient_thermal_model = ambient_thermal_model
        self.__electrolyzer = electrolyzer
        self.__HEAT_CAPACITY = self.__electrolyzer.get_heat_capacity_stack() # J/K
        self.__THERMAL_RESISTANCE = self.__electrolyzer.get_thermal_resistance_stack()
        self.__thermal_controller = IdealVarFlowThermalController(config, self.__HEAT_CAPACITY)
        self.__temperature_stack_1 = 0  # °C
        self.__NUMBER_CELLS = self.__electrolyzer.get_number_cells()
        self.__GEOM_AREA_STACK = self.__electrolyzer.get_geom_area_stack() # cm²
        self.__GEOM_AREA_CELL = self.__GEOM_AREA_STACK / self.__NUMBER_CELLS  # cm²
        self.__NOMINAL_STACK_POWER = self.__electrolyzer.get_nominal_stack_power()  # W
        self.__convection_heat = 0  # initialize variable
        self.__heat_generation = 0  # initialize variable
        self.__TH_NEUT_VOLTAGE = 286 * 10 ** 3 / (2 * ConstantsHydrogen.FARADAY_CONST)  # V
        self.__AMOUNT_WATER = self.__electrolyzer.get_water_in_stack() # kg
        self.__h2o_flow_stack = 0  # mol/s
        self.__heat_h2o = 0  #
        self.max_water_flow_stack = self.calculate_max_water_flow_stack(self.__NOMINAL_STACK_POWER)  # mol/s
        self.min_water_flow_stack = 0.1 * self.max_water_flow_stack  # mol/s
        self.__pump = pump
        self.pump_power = 0  # W
        self.__water_heating = water_heating

    def calculate(self, time: float, state: ElectrolyzerState, pressure_cathode_0, pressure_anode_0) -> None:
        timestep = time - state.time
        ambient_temperature = self.__ambient_thermal_model.get_temperature(time) - 273.15  # K -> °C
        temperature_stack_0 = state.temperature  # °C
        current_dens = state.current / self.__GEOM_AREA_CELL # A/cm²
        sat_p_h2o = state.sat_pressure_h2o  # bar
        h2_genearation_per_area = state.hydrogen_production / self.__GEOM_AREA_STACK  # mol/s/cm²
        o2_generation_per_area = state.oxygen_production / self.__GEOM_AREA_STACK  # mol/s/cm²
        h2o_use_per_area = state.water_use / self.__GEOM_AREA_STACK  # mol/s/cm²

        # water gives all its heat energy to the stack
        temperature_h2o_out = temperature_stack_0  # °C

        # specific heat generation in electrolyzer cell
        heat_cell = self.calculate_heat_cell(state.voltage, state.current)

        # specific heat sink because of freshwater
        spec_heat_fresh_water = self.calculate_spec_heat_freshwater(h2o_use_per_area, temperature_h2o_out,
                                                                    ambient_temperature)

        # heat loss to ambient
        delta_temp = temperature_stack_0 - ambient_temperature
        heat_loss_ambient = (1 / self.__THERMAL_RESISTANCE) * delta_temp

        # total heat generation electrolyzer stack
        heat_stack = heat_cell*self.__NUMBER_CELLS + spec_heat_fresh_water * self.__GEOM_AREA_STACK - heat_loss_ambient # W

        # calculation of watertemperature and waterflow for tempering the stack
        self.__thermal_controller.calculate(temperature_stack_0, heat_stack, timestep, self.min_water_flow_stack, current_dens)
        temperature_h2o_in = temperature_stack_0 + self.__thermal_controller.get_delta_water_temp_in()  # °C
        self.__h2o_flow_stack = self.__thermal_controller.get_h2o_flow()  # mol/s
        self.__heat_h2o = self.calculate_heat_h2o(self.__h2o_flow_stack, temperature_h2o_in, temperature_h2o_out)

        # temperature calculation stack
        if self.__thermal_controller.get_heat_control_on():
            self.__temperature_stack_1 = temperature_stack_0 + timestep / self.__HEAT_CAPACITY * (heat_stack + self.__heat_h2o)  # °C
            # if heat control is on, water is circulated through the stack and controls the temperature of the stack
            # with its own temperature-> heat capacity of water is not accounted
        else:
            self.__temperature_stack_1 = temperature_stack_0 + timestep / (self.__HEAT_CAPACITY + self.__AMOUNT_WATER *
                                                                           ConstantsHydrogen.HEAT_CAPACITY_WATER) * \
                                                                        (heat_stack + self.__heat_h2o)  # °C
            # if heat control is off there is no water circulation -> heat capacity of water which remains in the stack
            # needs to be accounted for the cooling process

        # convection heat: heat that is transported to the ambient area
        if self.__heat_h2o < 0:
            self.__convection_heat = heat_loss_ambient * self.__NUMBER_CELLS - self.__heat_h2o
        else:
            self.__convection_heat = heat_loss_ambient * self.__NUMBER_CELLS

    def calculate_spec_heat_freshwater(self, h2o_use_per_area, temp_h2o_in, temp_ambient) -> float:
        """ calculates the cooling effect of the feedwater
        if temp_h2o_in > temp_ambient: feedwater cools the water in the circulation"""
        delta_temp = temp_ambient - temp_h2o_in
        return ConstantsHydrogen.HEAT_CAPACITY_WATER * h2o_use_per_area * ConstantsHydrogen.MOLAR_MASS_WATER * delta_temp

    def calculate_heat_h2o(self, h2o_flow_stack, temp_h2o_in, temp_h2o_out) -> float:
        delta_temp = temp_h2o_in - temp_h2o_out
        self.__water_heating.calculate_heating_power(h2o_flow_stack, delta_temp)
        return self.__water_heating.get_heating_power()

    def calculate_heat_generation_cell(self, cell_voltage, current) -> float:
        return (cell_voltage / self.__NUMBER_CELLS - self.__TH_NEUT_VOLTAGE) * current

    def calculate_heat_cell(self, cell_voltage, current) -> float:
        heat_gen_cell = self.calculate_heat_generation_cell(cell_voltage, current)
        return heat_gen_cell

    def calculate_max_water_flow_stack(self, electrolyzer_nominal_power):
        """ calculates max water flow the cooling pump can provide in dependency of nominal power of electrolyzer
        based on data from thesis: PEM-Elektrolyse-Systeme zur Anwendung in Power-to-Gas Anlagen"""
        # max water flow rate = 1.5 kg/s for a 1250 kW EL-Stack
        water_flow_rate = 11.9 / 1250  # 11.9 kg/s / 1250 kW
        el_nom_power_kW = electrolyzer_nominal_power / 1000  # W -> kW
        return water_flow_rate * el_nom_power_kW / ConstantsHydrogen.MOLAR_MASS_WATER  #     mol/s

    def calculate_pump_power(self, water_flow_stack) -> None:
        # relative_flow = water_flow_stack / self.max_water_flow_stack
        # pressure_loss = 1.985 * 10 ** (-4) * (relative_flow * 100) ** 2 * 10 ** (5) # N/m²
        # volume_flow = water_flow_stack * ConstantsHydrogen.MOLAR_MASS_WATER / ConstantsHydrogen.DENSITY_WATER  # m³/s
        # self.__pump.calculate_pump_power(volume_flow * pressure_loss)  # W
        # self.pump_power = self.__pump.get_pump_power()
        pass

    def get_temperature(self) -> float:
        return self.__temperature_stack_1

    def get_water_flow_stack(self) -> float:
        return self.__h2o_flow_stack

    def get_power_water_heating(self) -> float:
        return self.__heat_h2o

    def get_pump_power(self) -> float:
        return self.pump_power

    def get_convection_heat(self) -> float:
        return self.__convection_heat


