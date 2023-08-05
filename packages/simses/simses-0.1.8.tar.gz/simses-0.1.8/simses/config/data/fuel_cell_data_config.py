from simses.config.data.data_config import DataConfig
from simses.constants_simses import ROOT_PATH


class FuelCellDataConfig(DataConfig):

    def __init__(self, path: str = None):
        super().__init__(path)
        self.__section: str = 'FUEL_CELL_DATA'

    @property
    def fuel_cell_data_dir(self) -> str:
        """Returns directory of fuelcell data files"""
        return ROOT_PATH + self.get_property(self.__section, 'FUEL_CELL_DATA_DIR')

    @property
    def pem_fuel_cell_pc_file(self) -> str:
        """Returns filename for polarisation curve for PEM-Fuelcell"""
        return self.fuel_cell_data_dir + self.get_property(self.__section, 'PEM_FUEL_CELL_PC_FILE')

    @property
    def pem_fuel_cell_power_file(self) -> str:
        """Returns filename for power curve for PEM-Fuelcell"""
        return self.fuel_cell_data_dir + self.get_property(self.__section, 'PEM_FUEL_CELL_POWER_FILE')
