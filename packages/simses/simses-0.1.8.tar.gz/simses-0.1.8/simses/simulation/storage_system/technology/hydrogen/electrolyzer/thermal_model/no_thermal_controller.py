from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_controller import \
    ThermalController


class NoThermalController(ThermalController):

    def __init__(self):
        super().__init__()

    def calculate(self, stack_temperature, heat_stack, timestep, min_water_flow_rate, current_dens) -> None:
        pass

    def get_h2o_flow(self) -> float:
        return 0.0

    def get_delta_water_temp_in(self) -> float:
        return 25.0

    def get_heat_control_on(self) -> bool:
        pass