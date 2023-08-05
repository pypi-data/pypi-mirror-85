from configparser import ConfigParser

from simses.commons.log import Logger
from simses.commons.state.technology.electrolyzer_state import ElectrolyzerState
from simses.config.data.electrolyzer_data_config import ElectrolyzerDataConfig
from simses.config.simulation.electrolyzer_config import ElectrolyzerConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.auxiliary.pump.pump import Pump
from simses.simulation.storage_system.auxiliary.water_heating.water_heating import WaterHeating
from simses.simulation.storage_system.technology.hydrogen.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.no_degradation_model import \
    NoDegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.pem_el_multi_dim_analytic_degradation_model import \
    PemElMultiDimAnalyticDegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.pem_el_multi_dim_analytic_degradation_model_ptl_couting import \
    PemElMultiDimAnalyticDegradationModelPtlCoating
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.no_pressure_model import \
    NoPressureModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_model import \
    PressureModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.var_cathode_pressure_model_el import \
    VarCathodePressureModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_model_alkaline import \
    AlkalinePressureModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.alkaline_electrolyzer_model.alkaline_electrolyzer_model import \
    AlkalineElectrolyzer
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.electrolyzer_stack_model import \
    ElectrolyzerStackModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.no_electrolyzer import NoElectrolyzer
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.pem_electrolyzer import \
    PemElectrolyzer
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.pem_electrolyzer_multi_dim_analytic_model.pem_electrolyzer_model import \
    PemElectrolyzerMultiDimAnalytic
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.pem_electrolyzer_multi_dim_analytic_model.pem_electrolyzer_model_ptl_coating import \
    PemElectrolyzerMultiDimAnalyticPtlCoating
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.no_thermal_model import \
    NoThermalModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.simple_thermal_model import \
    SimpleThermalModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.simple_thermal_model_alkaline import \
    SimpleThermalModelAlkaline
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_model import ThermalModel
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class ElectrolyzerFactory:

    def __init__(self, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__config_general: GeneralSimulationConfig = GeneralSimulationConfig(config)
        self.__config_electrolyzer: ElectrolyzerConfig = ElectrolyzerConfig(config)
        self.__config_electrolyzer_data: ElectrolyzerDataConfig = ElectrolyzerDataConfig()

    def create_state(self, system_id: int, storage_id: int, ambient_thermal_model: AmbientThermalModel,
                     electrolyzer: ElectrolyzerStackModel) -> ElectrolyzerState:
        state: ElectrolyzerState = ElectrolyzerState(system_id, storage_id)
        state.time = self.__config_general.start
        state.power = 0  # W
        state.temperature = ambient_thermal_model.get_initial_temperature() - 273.15  # K -> °C
        state.power_loss = 0  # W
        state.hydrogen_production = 0  # mol/s
        state.hydrogen_outflow = 0  # mol/s
        state.oxygen_production = 0  # mol/s
        state.fulfillment = 1.0  # p.u.
        state.soh = 1.0  # p.u.
        state.convection_heat = 0  # W
        state.resistance_increase_cyclic = 0  # p.u.
        state.resistance_increase_calendar = 0  # p.u.
        state.resistance_increase = 0  # p.u.
        state.exchange_current_decrease_cyclic = 1  # p.u.
        state.exchange_current_decrease_calendar = 1  # p.u.
        state.exchange_current_decrease = 1  # p.u.
        state.pressure_anode = ConstantsHydrogen.EPS  # barg
        state.pressure_cathode = ConstantsHydrogen.EPS  # barg
        state.sat_pressure_h2o = 0.03189409713071401  # bar  h2o saturation pressure at 25°C
        state.part_pressure_h2 = (1.0 + state.pressure_cathode) - 0.03189409713071401  # bar partial pressure h2 at 25°C and cathode pressure
        state.part_pressure_o2 = (1.0 + state.pressure_anode) - 0.03189409713071401  # bar partial pressure o2 at 25°C and anode pressure
        state.total_pressure = self.__config_electrolyzer.total_pressure
        state.water_use = 0  # mol/s#
        state.water_outflow_cathode = 0  # mol/s
        state.water_outflow_anode = 0  # mol/s
        state.water_flow = 0  # mol/s
        state.power_water_heating = 0  # W
        state.power_pump = 0  # W
        state.power_gas_drying = 0  # W
        state.power_compressor = 0  # W
        state.total_hydrogen_production = 0  # kg
        state.relative_time = 0  # start
        state.voltage = 1  # stays at 1 so that electrolyzer and fuel cell always see the power indepentently from the voltage a timestep before
        electrolyzer.calculate(state.power, state)
        state.voltage = electrolyzer.get_voltage()
        state.current = electrolyzer.get_current()
        state.current_density = electrolyzer.get_current_density()
        return state

    def create_electrolyzer_stack(self, electrolyzer: str, electrolyzer_maximal_power: float) -> ElectrolyzerStackModel:
        if electrolyzer == NoElectrolyzer.__name__:
            self.__log.debug('Creating electrolyzer as ' + electrolyzer)
            return NoElectrolyzer()
        elif electrolyzer == PemElectrolyzer.__name__:
            self.__log.debug('Creating electrolyzer as ' + electrolyzer)
            return PemElectrolyzer(electrolyzer_maximal_power, self.__config_electrolyzer_data)
        elif electrolyzer == PemElectrolyzerMultiDimAnalytic.__name__:
            self.__log.debug('Creating electrolyzer as ' + electrolyzer)
            return PemElectrolyzerMultiDimAnalytic(electrolyzer_maximal_power, self.__config_electrolyzer_data)
        elif electrolyzer == PemElectrolyzerMultiDimAnalyticPtlCoating.__name__:
            self.__log.debug('Creating electrolyzer as ' + electrolyzer)
            return PemElectrolyzerMultiDimAnalyticPtlCoating(electrolyzer_maximal_power, self.__config_electrolyzer_data)
        elif electrolyzer == AlkalineElectrolyzer.__name__:
            self.__log.debug('Creating electrolyzer as ' + electrolyzer)
            return AlkalineElectrolyzer(electrolyzer_maximal_power, self.__config_electrolyzer_data)
        else:
            options: [str] = list()
            options.append(PemElectrolyzer.__name__)
            raise Exception('Specified electrolyzer ' + electrolyzer + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_thermal_model(self, electrolyzer: ElectrolyzerStackModel, water_heating: WaterHeating, pump: Pump,
                             ambient_thermal_model: AmbientThermalModel) -> ThermalModel:
        # TODO For which electrolyzer do you want to include which thermal model?
        if type(electrolyzer).__name__ in [PemElectrolyzerMultiDimAnalytic.__name__,
                                     PemElectrolyzerMultiDimAnalyticPtlCoating.__name__]:
            self.__log.debug('Creating electrolyzer thermal model as ' + SimpleThermalModel.__name__)
            return SimpleThermalModel(electrolyzer, water_heating, pump, ambient_thermal_model, self.__config_electrolyzer)
        elif type(electrolyzer).__name__ == AlkalineElectrolyzer.__name__:
           self.__log.debug('Creating electrolyzer thermal model as ' + SimpleThermalModelAlkaline.__name__)
           return SimpleThermalModelAlkaline(electrolyzer, water_heating, pump, ambient_thermal_model,
                                     self.__config_electrolyzer)
        else:
            self.__log.debug('Creating electrolyzer thermal model as ' + NoThermalModel.__name__)
            return NoThermalModel()
        # else:
        #     options: [str] = list()
        #     options.append(SimpleThermalModelEl.__name__)
        #     raise Exception('Specified thermal model ' + thermal_model + 'is unknown. '
        #                                                                  'Following options are available: ' + str(
        #                                                                             options))

    def create_pressure_model(self, electrolyzer: ElectrolyzerStackModel) -> PressureModel:
        # TODO For which electrolyzer do you want to include which pressure model?
        if type(electrolyzer).__name__ in [PemElectrolyzerMultiDimAnalytic.__name__,
                                     PemElectrolyzerMultiDimAnalyticPtlCoating.__name__] :
            self.__log.debug('Creating electrolyzer pressure model as ' + VarCathodePressureModel.__name__)
            return VarCathodePressureModel(electrolyzer, self.__config_electrolyzer)
        elif type(electrolyzer).__name__ == AlkalineElectrolyzer.__name__:
            self.__log.debug('Creating electrolyzer pressure model as ' + AlkalineElectrolyzer.__name__)
            return AlkalinePressureModel()
        else:
            self.__log.debug('Creating electrolyzer pressure model as ' + NoPressureModel.__name__)
            return NoPressureModel()
        # else:
        #     options: [str] = list()
        #     options.append(VarCathodePressureModelEl.__name__)
        #     options.append(NoPressureModelEl.__name__)
        #     raise Exception('Specified thermal model ' + pressure_model_el + 'is unknown. '
        #                     'Following options are available: ' + str(options))

    def create_degradation_model(self, electrolyzer: ElectrolyzerStackModel):
        electrolyzer_name: str = type(electrolyzer).__name__
        if electrolyzer_name == PemElectrolyzerMultiDimAnalytic.__name__:
            self.__log.debug('Creating electrolyzer degradation model for ' + electrolyzer_name)
            return PemElMultiDimAnalyticDegradationModel(electrolyzer, self.__config_electrolyzer, self.__config_general)
        elif electrolyzer_name == PemElectrolyzerMultiDimAnalyticPtlCoating.__name__:
            self.__log.debug('Creating electrolyzer degradation model for ' + electrolyzer_name)
            return PemElMultiDimAnalyticDegradationModelPtlCoating(electrolyzer, self.__config_electrolyzer,
                                                                   self.__config_general)
        else:
            return NoDegradationModel()
            # options: [str] = list()
            # options.append(PemElMultiDimAnalyticDegradationModel.__name__)
            # options.append(PemElMultiDimAnalyticDegradationModelPtlCoating.__name__)
            # raise Exception('Specified electrolzyer degradation model ' + electrolyzer_name + 'is unknown. '
            #                 'Following options are available: ' + str(options))

    def close(self):
        self.__log.close()
