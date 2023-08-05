from abc import abstractmethod

from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.commons.state.technology.fuel_cell_state import FuelCellState
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.hydrogen_storage import HydrogenStorage


class Pipeline(HydrogenStorage):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate_inijected_hydrogen(self, time_diff, hydrogen_outflow) -> None:
        pass

    @abstractmethod
    def get_injected_hydrogen(self) -> float:
        pass

    @abstractmethod
    def get_tank_pressure(self) -> float:
        pass
