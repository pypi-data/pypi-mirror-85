from simses.simulation.storage_system.technology.hydrogen.fuel_cell.thermal_model.thermal_controller import \
    ThermalController


class NoThermalController(ThermalController):

    def __init__(self):
        super().__init__()

    def calculate_water_flow(self, stack_temperature, max_water_flow_cell, min_water_flow_cell) -> float:
        return 0

    def calculate_water_temperature_in(self, stack_temperature) -> float:
        return stack_temperature