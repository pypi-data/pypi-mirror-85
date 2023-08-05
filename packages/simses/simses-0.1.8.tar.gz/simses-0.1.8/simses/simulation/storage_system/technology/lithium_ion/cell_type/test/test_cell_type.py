from configparser import ConfigParser

import pytest
import numpy as np

from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.commons.utils.utils import all_non_abstract_subclasses_of
from simses.config.data.battery_data_config import BatteryDataConfig
from simses.config.simulation.battery_config import BatteryConfig
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.cell_type.lfp_sony import SonyLFP
from simses.simulation.storage_system.technology.lithium_ion.cell_type.generic_cell import GenericCell
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nca_panasonic_ncr import PanasonicNCA
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_molicel import MolicelNMC
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_sanyo_ur18650e import SanyoNMC
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_akasol_akm import AkasolAkmNMC
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_akasol_oem import AkasolOemNMC
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_field_data import FieldDataNMC

class TestCellType:
    # Single cell tests
    lithium_ion_state: LithiumIonState = LithiumIonState(0,0)
    step = 10
    test_values_soc = np.arange(0, 1.01, 1 / step)

    def make_lithium_ion_cell(self, lithium_ion_subclass):
        voltage = 0.1
        capacity = 0.1
        config: ConfigParser = ConfigParser()
        return lithium_ion_subclass(voltage, capacity, BatteryConfig(config=config), BatteryDataConfig())

    @pytest.fixture(scope="module") # module: gets only one instance
    def lithium_ion_subclass_list(self):
        return all_non_abstract_subclasses_of(CellType)

    @pytest.mark.parametrize("soc", test_values_soc)
    def test_ocv(self, soc, lithium_ion_subclass_list):
        for lithium_ion_subclass in lithium_ion_subclass_list:
            uut = self.make_lithium_ion_cell(lithium_ion_subclass)
            self.lithium_ion_state.soc = soc
            # all ocv values must be between the cell minimal voltage and maximum voltage
            assert uut.get_open_circuit_voltage(self.lithium_ion_state) >= uut.get_min_voltage()
            assert uut.get_open_circuit_voltage(self.lithium_ion_state) <= uut.get_max_voltage()
