from simses.config.data.fuel_cell_data_config import FuelCellDataConfig
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.stack_model.fuel_cell_stack_model import FuelCellStackModel


class JupiterFuelCell(FuelCellStackModel):

    def __init__(self, fuel_cell_maximal_power: float, fuel_cell_data_config: FuelCellDataConfig):
        super(JupiterFuelCell, self).__init__()

    def calculate(self, power) -> None:
        pass

    def get_current(self):
        pass

    def get_voltage(self):
        pass

    def get_hydrogen_consumption(self):
        pass

    def get_nominal_stack_power(self):
        pass

    def get_number_cells(self):
        pass

    def get_geom_area_stack(self):
        pass

    def get_heat_capactiy_stack(self):
        pass

    def close(self):
        pass
