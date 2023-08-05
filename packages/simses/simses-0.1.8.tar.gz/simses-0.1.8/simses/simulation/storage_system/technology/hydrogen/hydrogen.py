from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.log import Logger
from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.commons.state.technology.fuel_cell_state import FuelCellState
from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.technology.hydrogen.control.management import HydrogenManagementSystem
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.electrolyzer import Electrolyzer
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.fuel_cell import FuelCell
from simses.simulation.storage_system.technology.hydrogen.hydrogen_factory import HydrogenFactory
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.hydrogen_storage import HydrogenStorage
from simses.simulation.storage_system.technology.technology import StorageTechnology
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class Hydrogen(StorageTechnology):

    """
    Hydrogen is the top level class for coordinating all technologies related to hydrogen, i.e. electrolyzer, fuel cells
    and storage tank. It provides a management system for taking limitations into consideration. The hydrogen class
    requires always an electrolyzer, a fuel cell and a storage. In cases this circle is unwanted, dummy classes
    exists doing nothing, e.g. NoElectrolyzer or NoFuelCell.
    """

    def __init__(self, data_export: DataHandler, fuel_cell: str, fuel_cell_maximal_power: float, electrolyzer: str,
                 electrolyzer_maximal_power: float, storage: str, capacity: float, max_pressure: float,
                 ambient_thermal_model: AmbientThermalModel, system_id: int, storage_id: int, config: ConfigParser):
        super().__init__()
        self.__log = Logger(type(self).__name__)
        self.__electrolyzer: Electrolyzer = Electrolyzer(system_id, storage_id, electrolyzer,
                                                         electrolyzer_maximal_power, ambient_thermal_model,
                                                         config, data_export)
        self.__fuel_cell: FuelCell = FuelCell(system_id, storage_id, fuel_cell, fuel_cell_maximal_power,
                                              ambient_thermal_model, config, data_export)
        factory: HydrogenFactory = HydrogenFactory(config)
        if electrolyzer == "AlkalineElectrolyzer":
            electrolyzer_minimal_power = electrolyzer_maximal_power * 0.2
        else:
            electrolyzer_minimal_power = 0
        self.__management_system: HydrogenManagementSystem = factory.create_hydrogen_management_system(electrolyzer_minimal_power,
                                                                electrolyzer_maximal_power, fuel_cell_maximal_power)
        self.__hydrogen_storage: HydrogenStorage = factory.create_hydrogen_storage(storage, capacity, max_pressure)
        self.__hydrogen_state: HydrogenState = factory.create_hydrogen_state_from(system_id, storage_id)
        factory.close()
        self.__update_state(self.__hydrogen_state.time)

    def distribute_and_run(self, time: float, current: float, voltage: float):
        hs: HydrogenState = self.__hydrogen_state
        hs.power = current * voltage
        self.__management_system.update(time, hs)
        self.__electrolyzer.update(time, hs.power)
        self.__fuel_cell.update(time, hs.power)
        self.__hydrogen_storage.update_from(time - hs.time, self.__electrolyzer.state, self.__fuel_cell.state)
        self.__update_state(time)
        self.__log.info('Done with update')

    def __update_state(self, time: float) -> None:
        hydrogen_state: HydrogenState = self.__hydrogen_state
        electrolyzer_state: ElectrolyzerState = self.__electrolyzer.state
        fuel_cell_state: FuelCellState = self.__fuel_cell.state
        if hydrogen_state.is_charge:
            hydrogen_state.current = electrolyzer_state.current
            hydrogen_state.voltage = electrolyzer_state.voltage
            hydrogen_state.fulfillment *= electrolyzer_state.fulfillment
            hydrogen_state.power_loss = electrolyzer_state.power_loss
            hydrogen_state.temperature = electrolyzer_state.temperature
        else:
            hydrogen_state.current = fuel_cell_state.current
            hydrogen_state.voltage = fuel_cell_state.voltage
            hydrogen_state.fulfillment *= fuel_cell_state.fulfillment
            hydrogen_state.power_loss = fuel_cell_state.power_loss
            hydrogen_state.temperature = fuel_cell_state.temperature
        hydrogen_state.soc = self.__hydrogen_storage.get_soc()
        hydrogen_state.capacity = self.__hydrogen_storage.get_capacity()
        hydrogen_state.soh = electrolyzer_state.soh * fuel_cell_state.soh
        hydrogen_state.time = time

    @property
    def volume(self) -> float:
        return 0

    @property
    def mass(self) -> float:
        return 0

    @property
    def surface_area(self) -> float:
        return 0

    @property
    def specific_heat(self) -> float:
        return 0

    @property
    def convection_coefficient(self) -> float:
        return 0

    def wait(self):
        pass

    def get_auxiliaries(self) -> [Auxiliary]:
        aux: [Auxiliary] = list()
        aux.extend(self.__electrolyzer.get_auxiliaries())
        aux.extend(self.__fuel_cell.get_auxiliaries())
        aux.extend(self.__hydrogen_storage.get_auxiliaries())
        return aux

    @property
    def state(self):
        return self.__hydrogen_state

    def get_system_parameters(self) -> dict:
        return dict()

    def close(self):
        self.__management_system.close()
        self.__electrolyzer.close()
        self.__fuel_cell.close()
        self.__hydrogen_storage.close()
        self.__log.close()
