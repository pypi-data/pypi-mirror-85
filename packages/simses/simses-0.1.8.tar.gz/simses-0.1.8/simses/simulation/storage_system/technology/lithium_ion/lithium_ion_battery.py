from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.log import Logger
from simses.commons.state.system_parameters import SystemParameters
from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.technology.lithium_ion.battery_management_system.battery_management_system import \
    BatteryManagementSystem
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.degradation_model import DegradationModel
from simses.simulation.storage_system.technology.lithium_ion.equivalent_circuit_model.equivalent_circuit_model import \
    EquivalentCircuitModel
from simses.simulation.storage_system.technology.lithium_ion.lithium_ion_factory import LithiumIonFactory
from simses.simulation.storage_system.technology.technology import StorageTechnology
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class LithiumIonBattery(StorageTechnology):
    """Battery orchestrates its models for lithium_ion management system, degradation and thermal management as well as
    its equivalent circuit"""

    __ACCURACY = 1e-14
    __MAX_LOOPS = 10

    def __init__(self, cell: str, voltage: float, capacity: float, soh: float, data_export: DataHandler,
                 ambient_thermal_model: AmbientThermalModel,
                 storage_id: int, system_id: int, config: ConfigParser):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__factory: LithiumIonFactory = LithiumIonFactory(config)
        cell_type: CellType = self.__factory.create_cell_type(cell, voltage, capacity, soh)
        self.__cell_type: CellType = cell_type
        self.__battery_state: LithiumIonState = self.__factory.create_battery_state_from(system_id,
                                                                                         storage_id,
                                                                                         cell_type,
                                                                                         ambient_thermal_model)
        self.__degradation_model: DegradationModel = self.__factory.create_degradation_model_from(cell_type)
        self.__battery_management_system: BatteryManagementSystem = \
            self.__factory.create_battery_management_system_from(cell_type)
        self.__battery_model: EquivalentCircuitModel = self.__factory.create_battery_model_from(cell_type)
        self.__time: float = self.__battery_state.time
        self.__data_export: DataHandler = data_export
        self.__log.debug('created: ' + str(self.__battery_state))
        self.__data_export.transfer_data(self.__battery_state.to_export()) # initial timestep

    # def run(self) -> None:
    #     self.__updater_thread: Thread = Thread(target=self.update)
    #     self.__updater_thread.start()
    #
    # def join(self) -> None:
    #     self.__updater_thread.join()
    #     # pass

    def update(self) -> None:
        """Starting update of lithium_ion"""
        bs = self.__battery_state
        time = self.__time
        # Included loops for simultaneous current and voltage adjustment
        old_bs: LithiumIonState = LithiumIonState(0, 0)
        old_bs.set_all(bs)
        #power_target is necessary for BMS (fulfillmentfactor calculation)
        power_target: float = bs.current * bs.voltage
        for step in range(self.__MAX_LOOPS):
            bs.set_all(old_bs)
            self.__battery_management_system.update(time, bs, power_target)
            self.__battery_model.update(time, bs)
            bs.current = old_bs.voltage * bs.current / bs.voltage
            if abs(bs.voltage - old_bs.voltage) < self.__ACCURACY:
                break
            old_bs.current = bs.current
            old_bs.voltage = bs.voltage

        self.__degradation_model.update(time, bs)
        #TODO update battery temp in system thermal model
        bs.time = time
        self.__data_export.transfer_data(bs.to_export())

    def set(self, time: float, current: float) -> None:
        """
        Setting new state with input current for lithium_ion

        Parameters
        ----------
        time : current simulation timestamp
        current : current for lithium_ion in mA

        Returns
        -------

        """
        self.__battery_state.current = current
        self.__time = time

    def distribute_and_run(self, time: float, current: float, voltage: float):
        self.set(time, current)
        self.update()

    @property
    def volume(self) -> float:
        return self.__cell_type.get_volume()

    @property
    def mass(self) -> float:
        return self.__cell_type.get_mass()

    @property
    def surface_area(self) -> float:
        return self.__cell_type.get_surface_area()

    @property
    def specific_heat(self) -> float:
        return self.__cell_type.get_specific_heat()

    @property
    def convection_coefficient(self) -> float:
        return self.__cell_type.get_convection_coefficient()

    def wait(self):
        pass

    def get_auxiliaries(self) -> [Auxiliary]:
        return list()

    @property
    def state(self) -> LithiumIonState:
        return self.__battery_state

    def get_system_parameters(self) -> dict:
        parameters: dict = dict()
        parameters[SystemParameters.BATTERY_CIRCUIT] = str(self.__cell_type.get_serial_scale()) + 's' + \
                                                       str(self.__cell_type.get_parallel_scale()) + 'p'
        return parameters

    def close(self) -> None:
        """Closing all resources in lithium_ion"""
        self.__battery_management_system.close()
        self.__battery_model.close()
        self.__degradation_model.close()
        self.__factory.close()
        self.__log.close()
