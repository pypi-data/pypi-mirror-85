from simses.config.simulation.hydrogen_config import HydrogenConfig
from simses.simulation.storage_system.technology.hydrogen.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_controller import \
    ThermalController


class VarFlowThermalController(ThermalController):
    """
    This controller controls the temperature of the EL-stack by varing the input temperaure of the feeding water and
    in the second step adapt the mass flow of the water in order to reach the desired temperature
    """

    def __init__(self, hydrogen_config: HydrogenConfig):
        super().__init__()
        self.stack_temp_desire = hydrogen_config.desire_temperature_el # °C
        self.slope_faktor = - 1 / 5
        self.delta_water_temperature = 5  # K
        self.max_cooling_rate = 3  # K/s; assumption needs to be that high, so that there is no thermal runaway
        self.temperature_h2o_in = 0  # °C
        self.h2o_flow = 0  # mol/s#


    def calculate(self, stack_temperature, heat_stack, el_heat_capacity, timestep, min_water_flow_stack, current_dens) -> None:
        temp_diff = self.stack_temp_desire - stack_temperature

        # calculation of water temperature
        control_faktor = self.calculate_control_faktor_temperature(temp_diff)
        self.temperature_h2o_in = stack_temperature - control_faktor * self.delta_water_temperature

        # calculation of water flow
        if stack_temperature <= self.stack_temp_desire:
            return min_water_flow_stack
        else:
            ideal_cooling_rate = temp_diff / timestep
            if ideal_cooling_rate < self.max_cooling_rate:
                cooling_rate = ideal_cooling_rate
            else:
                cooling_rate = self.max_cooling_rate
            self.h2o_flow = el_heat_capacity * cooling_rate / (ConstantsHydrogen.HEAT_CAPACITY_WATER *
                                                               ConstantsHydrogen.MOLAR_MASS_WATER * temp_diff)

    def get_delta_water_temp_in(self) -> float:
        return self.temperature_h2o_in

    def get_h2o_flow(self) -> float:
        return self.h2o_flow

    def calculate_control_faktor_temperature(self, temp_diff) -> float:
        if abs(temp_diff) < 5:
            return self.slope_faktor * temp_diff
        else:
            return 1