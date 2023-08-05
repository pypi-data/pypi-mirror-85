from configparser import ConfigParser

from simses.commons.log import Logger
from simses.commons.state.technology.fuel_cell_state import FuelCellState
from simses.config.data.fuel_cell_data_config import FuelCellDataConfig
from simses.config.simulation.fuel_cell_config import FuelCellConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.technology.hydrogen.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model.no_pressure_model import \
    NoPressureModel
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model.pressure_model import \
    PressureModel
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.stack_model.fuel_cell_stack_model import \
    FuelCellStackModel
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.stack_model.jupiter_fuel_cell import JupiterFuelCell
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.stack_model.no_fuel_cell import NoFuelCell
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.stack_model.pem_fuel_cell import PemFuelCell
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.thermal_model.no_thermal_model import \
    NoThermalModel
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.thermal_model.thermal_model import ThermalModel
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class FuelCellFactory:

    def __init__(self, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__config_general: GeneralSimulationConfig = GeneralSimulationConfig(config)
        self.__config_fuel_cell: FuelCellConfig = FuelCellConfig(config)
        self.__config_fuel_cell_data: FuelCellDataConfig = FuelCellDataConfig()

    def create_state(self, system_id: int, storage_id: int, ambient_thermal_model: AmbientThermalModel,
                     fuel_cell: FuelCellStackModel) -> FuelCellState:
        state: FuelCellState = FuelCellState(system_id, storage_id)
        state.time = self.__config_general.start
        state.power = 0  # W
        state.temperature = ambient_thermal_model.get_initial_temperature() - 273.15  # K -> °C
        state.power_loss = 0  # W
        state.fulfillment = 1.0  # p.u.
        state.soh = 1.0  # p.u.
        state.convection_heat = 0  # W
        state.hydrogen_use = 0  # mols
        state.hydrogen_inflow = 0  # mol/s
        state.oxygen_use = 0  # mol/s
        state.oxygen_inflow = 0  # mol/s
        state.pressure_cathode = ConstantsHydrogen.EPS  # barg
        state.pressure_anode = ConstantsHydrogen.EPS  # barg
        state.voltage = 1  # stays at 1 so that electrolyzer and fuel cell always see the power indepentently from the voltage a timestep before
        fuel_cell.calculate(state.power)
        state.voltage = fuel_cell.get_voltage()
        state.current = fuel_cell.get_current()
        state.current_density = fuel_cell.get_current_density()
        return state

    def create_fuel_cell_stack(self, fuel_cell: str, fuel_cell_maximal_power: float) -> FuelCellStackModel:
        if fuel_cell == PemFuelCell.__name__:
            self.__log.debug('Creating fuel cell as ' + fuel_cell)
            return PemFuelCell(fuel_cell_maximal_power, self.__config_fuel_cell_data)
        elif fuel_cell == JupiterFuelCell.__name__:
            self.__log.debug('Creating fuel cell as ' + fuel_cell)
            return JupiterFuelCell(fuel_cell_maximal_power, self.__config_fuel_cell_data)
        elif fuel_cell == NoFuelCell.__name__:
            self.__log.debug('Creating fuel cell as ' + fuel_cell)
            return NoFuelCell(fuel_cell_maximal_power, self.__config_fuel_cell_data)
        else:
            options: [str] = list()
            options.append(PemFuelCell.__name__)
            options.append(JupiterFuelCell.__name__)
            options.append(NoFuelCell.__name__)
            raise Exception('Specified fuel cell ' + fuel_cell + ' is unknown. '
                                                                 'Following options are available: ' + str(options))

    def create_thermal_model(self, fuel_cell: FuelCellStackModel, ambient_thermal_model: AmbientThermalModel) -> ThermalModel:
        # TODO For which fuel cell do you want to include which thermal model?
        return NoThermalModel()
        # if thermal_model == NoThermalModelFc.__name__:
        #     self.__log.debug('Creating electrolyzer thermal model as ' + thermal_model)
        #     return NoThermalModelFc()
        # else:
        #     options: [str] = list()
        #     options.append(ThermalModelFc.__name__)
        #     raise Exception('Specified thermal model ' + thermal_model + 'is unknown. '
        #                     'Following options are available: ' + str(options))

    def create_pressure_model(self, fuel_cell: FuelCellStackModel) -> PressureModel:
        # TODO For which fuel cell do you want to include which pressure model?
        return NoPressureModel()
        # if pressure_model_fc == NoPressureModelFc.__name__:
        #     self.__log.debug('Creatubg electrolyzer pressure model as ' + pressure_model_fc)
        #     return NoPressureModelFc()
        # else:
        #     options: [str] = list()
        #     options.append(NoPressureModelFc.__name__)
        #     raise Exception('Specified thermal model ' + pressure_model_fc + 'is unknown. '
        #                                                                      'Following options are available: ' + str(
        #         options))

    def close(self):
        self.__log.close()
