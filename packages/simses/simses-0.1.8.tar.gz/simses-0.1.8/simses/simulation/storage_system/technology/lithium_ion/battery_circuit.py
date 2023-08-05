from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.commons.data.data_handler import DataHandler
from simses.commons.log import Logger
from simses.simulation.storage_system.technology.lithium_ion.lithium_ion_battery import LithiumIonBattery
from simses.simulation.storage_system.technology.lithium_ion.lithium_ion_factory import LithiumIonFactory
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.thermal_model.thermal_model import ThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.system_thermal_model import SystemThermalModel


class BatteryCircuit:

    __PARALLEL_IDX = 0
    __SERIAL = 1
    __PARALLEL = 1
    __SIMULATE_EACH_CELL = False

    def __init__(self, cell: str, voltage: float, capacity: float, thermal_model: str, data_export: DataHandler,
                 system_thermal_model: SystemThermalModel, storage_id: int, system_id: int):
        raise Exception("BatteryCircuit is deprecated")
        self.__log: Logger = Logger(type(self).__name__)
        factory: LithiumIonFactory = LithiumIonFactory()
        cell_type: CellType = factory.create_cell_type(cell, voltage, capacity)
        thermal_model: ThermalModel = factory.create_thermal_model_from(thermal_model, cell_type, system_thermal_model)
        self.__battery_string: [[LithiumIonBattery]] = list()
        if self.__SIMULATE_EACH_CELL:
            for s in range(self.__SERIAL):
                serial_batteries: [LithiumIonBattery] = list()
                for p in range(self.__SERIAL):
                    # TODO this will not work (MM)
                    position: list = [str(system_id), str(storage_id), str(p + 1), str(s + 1)]
                    serial_batteries.append(LithiumIonBattery(cell_type, data_export, thermal_model, position=position))
                self.__battery_string.append(serial_batteries)
        else:
            position: list = [system_id, storage_id]
            self.__battery_string.append([LithiumIonBattery(cell_type, data_export, thermal_model, position)])
        self.__log.debug('serial:   ' + str(len(self.__battery_string)))
        self.__log.debug('parallel: ' + str(len(self.__battery_string[self.__PARALLEL_IDX])))
        self.__log.debug('simulate each cell: ' + str(self.__SIMULATE_EACH_CELL))
        self.__log.debug('created')

    def distribute_and_run(self, time: float, current: float, voltage: float) -> None:
        voltage = self.state.voltage
        for parallel_batteries in self.__battery_string:
            size = len(parallel_batteries)
            for battery in parallel_batteries:
                # TODO improve current distribution to batteries, interface to OparaBatt (Philipp Jocher)
                # 1st approach: equal distribution of current
                # lithium_ion.set(time, current / size)
                # 2nd approach: current distribution is voltage dependent (OCV + RINT)
                battery.set(time, current * battery.state.voltage / voltage)
                # 3rd approach: Jaehyung Lee, A novel li-ion lithium_ion pack modeling considerging single cell information and capacity variation, https://doi.org/10.1109/ECCE.2017.8096880
                # start calculation for lithium_ion parameters
                battery.run() if self.__SIMULATE_EACH_CELL else battery.update()

    def wait(self) -> None:
        if not self.__SIMULATE_EACH_CELL:
            return
        for parallel_batteries in self.__battery_string:
            for battery in parallel_batteries:
                battery.join()

    @property
    def state(self) -> LithiumIonState:
        serial_states = []
        for parallel_batteries in self.__battery_string:
            parallel_states = []
            for battery in parallel_batteries:
                parallel_states.append(battery.state)
            serial_states.append(LithiumIonState.sum_parallel(parallel_states))
        return LithiumIonState.sum_serial(serial_states)

    def close(self) -> None:
        """Closing all resources in lithium_ion circuit"""
        self.__log.close()
        for parallel_batteries in self.__battery_string:
            for battery in parallel_batteries:
                battery.close()
