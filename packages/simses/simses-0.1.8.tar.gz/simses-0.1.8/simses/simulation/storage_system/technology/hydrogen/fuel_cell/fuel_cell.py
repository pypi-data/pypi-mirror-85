from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.state.technology.fuel_cell_state import FuelCellState
from simses.simulation.storage_system.auxiliary.pump.fixeta_centrifugal_pump import FixEtaCentrifugalPump
from simses.simulation.storage_system.auxiliary.pump.pump import Pump
from simses.simulation.storage_system.auxiliary.water_heating.water_heating import WaterHeating
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.fuel_cell_factory import FuelCellFactory
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model.pressure_model import PressureModel
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.stack_model.fuel_cell_stack_model import \
    FuelCellStackModel
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.stack_model.no_fuel_cell import NoFuelCell
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.thermal_model.thermal_model import ThermalModel
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class FuelCell:

    """
    FuelCell is the top level class incorporating a FuelCellStackModel, a ThermalModel and a PressureModel. The
    specific classes are instantiated within the FuelCellFactory.
    """

    __PUMP_EFFICIENCY: float = 0.7

    def __init__(self, system_id: int, storage_id: int, fuel_cell: str, max_power: float,
                 ambient_thermal_model: AmbientThermalModel, config: ConfigParser, data_handler: DataHandler):
        super().__init__()
        self.__data_handler: DataHandler = data_handler
        self.__pump: Pump = FixEtaCentrifugalPump(self.__PUMP_EFFICIENCY)
        self.__water_heating: WaterHeating = WaterHeating()
        factory: FuelCellFactory = FuelCellFactory(config)
        self.__stack_model: FuelCellStackModel = factory.create_fuel_cell_stack(fuel_cell, max_power)
        self.__pressure_model: PressureModel = factory.create_pressure_model(self.__stack_model)
        self.__thermal_model: ThermalModel = factory.create_thermal_model(self.__stack_model, ambient_thermal_model)
        self.__state: FuelCellState = factory.create_state(system_id, storage_id, ambient_thermal_model, self.__stack_model)
        factory.close()
        self.__log_data: bool = not isinstance(self.__stack_model, NoFuelCell)
        self.__write_data()

    def update(self, time: float, power: float) -> None:
        """
        Updates current, voltage and hydrogen flow of hydrogen state

        Parameters
        ----------
        time :
        state :
        power :

        Returns
        -------

        """
        local_power = power if power < 0.0 else 0.0
        state: FuelCellState = self.__state
        self.__stack_model.update(local_power, state)
        self.__pressure_model.update(time, state)
        self.__thermal_model.update(time, state)
        state.time = time
        self.__write_data()

    def __write_data(self) -> None:
        if self.__log_data:
            self.__data_handler.transfer_data(self.__state.to_export())

    def get_auxiliaries(self) -> list:
        return list()

    @property
    def state(self) -> FuelCellState:
        return self.__state

    def close(self):
        self.__stack_model.close()
        self.__pressure_model.close()
        self.__thermal_model.close()
        self.__pump.close()
        self.__water_heating.close()
