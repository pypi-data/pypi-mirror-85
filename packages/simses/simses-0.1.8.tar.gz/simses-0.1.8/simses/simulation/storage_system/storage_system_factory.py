import os
from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.log import Logger
from simses.commons.state.system_state import SystemState
from simses.config.data.power_electronics_config import PowerElectronicsConfig
from simses.config.data.temperature_data_config import TemperatureDataConfig
from simses.config.simulation.battery_config import BatteryConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig
from simses.config.simulation.storage_system_config import StorageSystemConfig
from simses.simulation.storage_system.auxiliary.heating_ventilation_air_conditioning.fix_cop_hvac import \
    FixCOPHeatingVentilationAirConditioning
from simses.simulation.storage_system.auxiliary.heating_ventilation_air_conditioning.fix_cop_hvac_pid_control import \
    FixCOPHeatingVentilationAirConditioningPIDControl
from simses.simulation.storage_system.auxiliary.heating_ventilation_air_conditioning.hvac import \
    HeatingVentilationAirConditioning
from simses.simulation.storage_system.auxiliary.heating_ventilation_air_conditioning.no_hvac import \
    NoHeatingVentilationAirConditioning
from simses.simulation.storage_system.control.equal_power_distributor import EqualPowerDistributor
from simses.simulation.storage_system.control.power_distributor import PowerDistributor
from simses.simulation.storage_system.control.soc_based_power_distributor import SocBasedPowerDistributor
from simses.simulation.storage_system.dc_coupling.bus_charging_dc_coupling import BusChargingDcCoupling
from simses.simulation.storage_system.dc_coupling.bus_charging_profile import BusChargingProfileDcCoupling
from simses.simulation.storage_system.dc_coupling.dc_coupling import DcCoupling
from simses.simulation.storage_system.dc_coupling.no_dc_coupling import NoDcCoupling
from simses.simulation.storage_system.dc_coupling.usp_dc_coupling import USPDCCoupling
from simses.simulation.storage_system.housing.housing import Housing
from simses.simulation.storage_system.housing.no_housing import NoHousing
from simses.simulation.storage_system.housing.twenty_ft_container import TwentyFtContainer
from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter import AcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter_identical_stacked import \
    AcDcConverterIdenticalStacked
from simses.simulation.storage_system.power_electronics.acdc_converter.bonfiglioli_notton_acdc_converter import \
    BonfiglioliAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.field_data_acdc_converter import \
    FieldDataAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.fix_efficiency_acdc_converter import \
    FixEfficiencyAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.no_loss_acdc_converter import NoLossAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.notton_acdc_converter import NottonAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.notton_loss_acdc_converter import \
    NottonLossAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.sinamics_acdc_converter import \
    Sinamics120AcDcConverter
from simses.simulation.storage_system.power_electronics.dcdc_converter.dcdc_converter import DcDcConverter
from simses.simulation.storage_system.power_electronics.dcdc_converter.no_loss_dcdc_converter import NoLossDcDcConverter
from simses.simulation.storage_system.power_electronics.power_electronics import PowerElectronics
from simses.simulation.storage_system.storage_system_ac import StorageSystemAC
from simses.simulation.storage_system.storage_system_dc import StorageSystemDC
from simses.simulation.storage_system.technology import lithium_ion, hydrogen, redox_flow
from simses.simulation.storage_system.technology.hydrogen.hydrogen import Hydrogen
from simses.simulation.storage_system.technology.lithium_ion.lithium_ion_battery import LithiumIonBattery
from simses.simulation.storage_system.technology.redox_flow.redox_flow_system import RedoxFlow
from simses.simulation.storage_system.technology.technology import StorageTechnology
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.constant_ambient_temperature import \
    ConstantAmbientTemperature
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.location_ambient_temperature import \
    LocationAmbientTemperature
from simses.simulation.storage_system.thermal_model.system_thermal_model.no_system_thermal_model import \
    NoSystemThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.system_thermal_model import \
    SystemThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.zero_d_dynamic_system_thermal_model import \
    ZeroDDynamicSystemThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.zero_d_system_thermal_model import \
    ZeroDSystemThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.zero_d_system_thermal_model_single_step import \
    ZeroDSystemThermalModelSingleStep


class StorageSystemFactory:

    """
    The StorageSystemFactory instantiates all necessary and configured objects for AC and DC storage systems.
    """

    __lithium_ion_name: str = lithium_ion.__name__.split('.')[-1]
    __hydrogen_name: str = hydrogen.__name__.split('.')[-1]
    __redox_flow_name: str = redox_flow.__name__.split('.')[-1]

    def __init__(self, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__simulation_config: ConfigParser = config
        self.__system_config: StorageSystemConfig = StorageSystemConfig(config)
        self.__general_config: GeneralSimulationConfig = GeneralSimulationConfig(config)
        self.__temperature_config: TemperatureDataConfig = TemperatureDataConfig()
        self.__power_electronics_data_config: PowerElectronicsConfig = PowerElectronicsConfig()
        self.__profile_config: ProfileConfig = ProfileConfig(config)
        self.__config_battery: BatteryConfig = BatteryConfig(config)

    def create_acdc_converter(self, converter: str, max_power: float,
                              intermediate_cicuit_voltage: float) -> AcDcConverter:
        converter_configuration: dict = self.__system_config.acdc_converter
        converter_type = converter_configuration[converter][StorageSystemConfig.ACDC_CONVERTER_TYPE]
        acdc_converter: AcDcConverter = None
        if converter_type == NoLossAcDcConverter.__name__:
            self.__log.debug('Creating acdc converter as ' + converter_type)
            acdc_converter = NoLossAcDcConverter(max_power)
        elif converter_type == NottonAcDcConverter.__name__:
            self.__log.debug('Creating acdc converter as ' + converter_type)
            acdc_converter = NottonAcDcConverter(max_power)
        elif converter_type == FixEfficiencyAcDcConverter.__name__:
            self.__log.debug('Creating acdc converter as ' + converter_type)
            acdc_converter = FixEfficiencyAcDcConverter(max_power)
        elif converter_type == Sinamics120AcDcConverter.__name__:
            self.__log.debug('Creating acdc converter as ' + converter_type)
            acdc_converter = Sinamics120AcDcConverter(max_power, self.__power_electronics_data_config)
        elif converter_type == FieldDataAcDcConverter.__name__:
            self.__log.debug('Creating acdc converter as ' + converter_type)
            acdc_converter = FieldDataAcDcConverter(max_power)
        elif converter_type == BonfiglioliAcDcConverter.__name__:
            self.__log.debug('Creating acdc converter as ' + converter_type)
            acdc_converter = BonfiglioliAcDcConverter(max_power)
        else:
            options: [str] = list()
            options.append(NoLossAcDcConverter.__name__)
            options.append(NottonAcDcConverter.__name__)
            options.append(NottonLossAcDcConverter.__name__)
            options.append(FixEfficiencyAcDcConverter.__name__)
            options.append(Sinamics120AcDcConverter.__name__)
            options.append(FieldDataAcDcConverter.__name__)
            options.append(BonfiglioliAcDcConverter.__name__)
            raise Exception('ACDC converter ' + converter_type + ' is unknown. '
                                                                 'Following options are available: ' + str(options))
        return self.create_stacked_acdc_converter(converter, acdc_converter)

    def create_stacked_acdc_converter(self, converter: str, acdc_converter: AcDcConverter) -> AcDcConverter:
        try:
            converter_configuration: dict = self.__system_config.acdc_converter
            number_converters: int = int(converter_configuration[converter][StorageSystemConfig.ACDC_CONVERTER_NUMBERS])
            if number_converters > 1:
                switch_value: float = 1.0
                return AcDcConverterIdenticalStacked(number_converters, switch_value,
                                                     acdc_converter, self.__power_electronics_data_config)
        except IndexError:
            pass
        return acdc_converter

    def create_dcdc_converter(self, converter: str, intermediate_circuit_voltage: float) -> DcDcConverter:
        converter_configuration: dict = self.__system_config.dcdc_converter
        converter_type = converter_configuration[converter][StorageSystemConfig.DCDC_CONVERTER_TYPE]
        if converter_type == NoLossDcDcConverter.__name__:
            self.__log.debug('Creating dcdc converter as ' + converter_type)
            return NoLossDcDcConverter(intermediate_circuit_voltage)
        else:
            options: [str] = list()
            options.append(NoLossDcDcConverter.__name__)
            raise Exception('DCDC converter ' + converter_type + ' is unknown. '
                                                                 'Following options are available: ' + str(options))

    def create_ambient_temperature_model(self) -> AmbientThermalModel:
        ambient_temperature_model: str = str(self.__system_config.ambient_temperature_model[StorageSystemConfig.AMBIENT_TEMPERATURE_MODEL])
        if ambient_temperature_model == ConstantAmbientTemperature.__name__:
            self.__log.debug('Creating ambient temperature model as ' + ambient_temperature_model)
            try:
                constant_ambient_temperature: float = float(self.__system_config.ambient_temperature_model[StorageSystemConfig.AMBIENT_TEMPERATURE_CONSTANT])
                return ConstantAmbientTemperature(constant_ambient_temperature)
            except IndexError:
                self.__log.debug('Creating ambient temperature model as ' + ambient_temperature_model + 'with default value of constant ambient temperature = 25°C.')
                return ConstantAmbientTemperature()
        elif ambient_temperature_model == LocationAmbientTemperature.__name__:
            self.__log.debug('Creating ambient temperature model as ' + ambient_temperature_model)
            return LocationAmbientTemperature(self.__temperature_config, self.__general_config)
        else:
            options: [str] = list()
            options.append(ConstantAmbientTemperature.__name__)
            options.append(LocationAmbientTemperature.__name__)
            raise Exception('Ambient temperature model ' + ambient_temperature_model + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_thermal_model_from(self, thermal_model: str, hvac: HeatingVentilationAirConditioning,
                                  ambient_thermal_model: AmbientThermalModel, housing: Housing,
                                  dc_systems: [StorageSystemDC], ac_dc_converter: AcDcConverter) -> SystemThermalModel:
        if thermal_model == NoSystemThermalModel.__name__:
            self.__log.debug('Creating thermal model for cell type ' + NoSystemThermalModel.__class__.__name__)
            return NoSystemThermalModel(ambient_thermal_model, self.__general_config)
        elif thermal_model == ZeroDDynamicSystemThermalModel.__name__:
            self.__log.debug('Creating thermal model for cell type ' + thermal_model.__class__.__name__)
            return ZeroDDynamicSystemThermalModel(ambient_thermal_model, housing, hvac, self.__general_config,
                                                  self.__system_config, dc_systems, ac_dc_converter)
        elif thermal_model == ZeroDSystemThermalModel.__name__:
            self.__log.debug('Creating thermal model for cell type ' + thermal_model.__class__.__name__)
            return ZeroDSystemThermalModel(ambient_thermal_model, housing, hvac, self.__general_config,
                                           self.__system_config, dc_systems, ac_dc_converter)
        elif thermal_model == ZeroDSystemThermalModelSingleStep.__name__:
            self.__log.debug('Creating thermal model for cell type ' + thermal_model.__class__.__name__)
            return ZeroDSystemThermalModelSingleStep(ambient_thermal_model, housing, hvac, self.__general_config,
                                                     dc_systems, ac_dc_converter)

        else:
            options: [str] = list()
            options.append(NoSystemThermalModel.__name__)
            options.append(ZeroDSystemThermalModelSingleStep.__name__)
            raise Exception('System temperature model ' + thermal_model + ' is unknown. '
                                                                          'Following options are available: ' + str(
                options))

    def create_housing_from(self, housing_name: str, ambient_thermal_model: AmbientThermalModel) -> Housing:
        if housing_name == NoHousing.__name__:
            return NoHousing(ambient_thermal_model)
        elif housing_name == TwentyFtContainer.__name__:
            return TwentyFtContainer(ambient_thermal_model)
        else:
            options: [str] = list()
            options.append(NoHousing.__name__)
            options.append(TwentyFtContainer.__name__)
            raise Exception('Housing model ' + housing_name + ' is unknown. '
                                                              'Following options are available: ' + str(options))

    def create_hvac_from(self, hvac: str) -> HeatingVentilationAirConditioning:
        hvac_configuration: dict = self.__system_config.hvac
        hvac_type = hvac_configuration[hvac][StorageSystemConfig.HVAC_TYPE]
        if hvac_type == NoHeatingVentilationAirConditioning.__name__:
            return NoHeatingVentilationAirConditioning()
        elif hvac_type == FixCOPHeatingVentilationAirConditioning.__name__:
            return FixCOPHeatingVentilationAirConditioning(hvac_configuration)
        elif hvac_type == FixCOPHeatingVentilationAirConditioningPIDControl.__name__:
            return FixCOPHeatingVentilationAirConditioningPIDControl(hvac_configuration)
        else:
            options: [str] = list()
            options.append(NoHeatingVentilationAirConditioning.__name__)
            options.append(FixCOPHeatingVentilationAirConditioning.__name__)
            raise Exception('HVAC model ' + hvac_type + ' is unknown. '
                                                        'Following options are available: ' + str(options))

    def create_system_state_from(self, system_id, storage_id) -> SystemState:
        state = SystemState(system_id, storage_id)
        state.set(SystemState.TIME, self.__general_config.start)
        state.set(SystemState.FULFILLMENT, 1.0)
        return state

    def create_power_distributor_ac(self) -> PowerDistributor:
        power_distributor_type: str = self.__system_config.power_distributor_ac
        return self.__create_power_distributor_from(power_distributor_type)

    def create_power_distributor_dc(self) -> PowerDistributor:
        power_distributor_type: str = self.__system_config.power_distributor_dc
        return self.__create_power_distributor_from(power_distributor_type)

    def __create_power_distributor_from(self, power_distributor_type: str) -> PowerDistributor:
        if power_distributor_type == EqualPowerDistributor.__name__:
            return EqualPowerDistributor()
        elif power_distributor_type == SocBasedPowerDistributor.__name__:
            return SocBasedPowerDistributor()
        else:
            options: [str] = list()
            options.append(EqualPowerDistributor.__name__)
            options.append(SocBasedPowerDistributor.__name__)
            raise Exception('Power distributor ' + power_distributor_type + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_storage_systems_ac(self, data_export: DataHandler) -> [StorageSystemAC]:
        ambient_thermal_model: AmbientThermalModel = self.create_ambient_temperature_model()
        # TODO location solar irradiation model
        ac_systems: [[str]] = self.__system_config.storage_systems_ac
        res: [StorageSystemAC] = list()
        names: [str] = list()
        id_number: int = 0
        for system in ac_systems:
            id_number += 1
            name = system[StorageSystemConfig.AC_SYSTEM_NAME]
            if name in names:
                raise Exception('Storage system name ' + name + ' is not unique.')
            names.append(name)
            power: float = float(system[StorageSystemConfig.AC_SYSTEM_POWER])
            intermediate_circuit_voltage: float = float(system[StorageSystemConfig.AC_SYSTEM_DC_VOLTAGE])
            converter: str = system[StorageSystemConfig.AC_SYSTEM_CONVERTER]
            thermal_model: str = system[StorageSystemConfig.AC_SYSTEM_THERMAL_MODEL]
            housing: str = system[StorageSystemConfig.AC_SYSTEM_HOUSING]
            hvac: str = system[StorageSystemConfig.AC_SYSTEM_HVAC]
            acdc_converter: AcDcConverter = self.create_acdc_converter(converter, power, intermediate_circuit_voltage)
            housing_model: Housing = self.create_housing_from(housing, ambient_thermal_model)
            heating_cooling: HeatingVentilationAirConditioning = self.create_hvac_from(hvac)
            power_distributor: PowerDistributor = self.create_power_distributor_dc()
            power_electronics: PowerElectronics = PowerElectronics(acdc_converter)
            dc_systems: [StorageSystemDC] = self.create_storage_systems_dc(name, data_export, ambient_thermal_model,
                                                                           intermediate_circuit_voltage, id_number)
            system_thermal_model: SystemThermalModel = self.create_thermal_model_from(thermal_model, heating_cooling,
                                                                                      ambient_thermal_model,
                                                                                      housing_model, dc_systems,
                                                                                      acdc_converter)

            state = self.create_system_state_from(id_number, 0)
            dc_couplings: [DcCoupling] = self.create_dc_couplings(name)
            res.append(StorageSystemAC(state, data_export, system_thermal_model, power_electronics, dc_systems,
                                       dc_couplings, housing_model, power_distributor))
        return res

    def create_dc_couplings(self, name: str) -> [DcCoupling]:
        dc_systems: [[str]] = self.__system_config.storage_systems_dc
        res: [DcCoupling] = list()
        for dc_system in dc_systems:
            system = dc_system[0]
            dc_type: str = dc_system[1]
            if system == name and DcCoupling.__name__ in dc_type:
                if dc_type == NoDcCoupling.__name__:
                    res.append(NoDcCoupling())
                elif dc_type == BusChargingDcCoupling.__name__:
                    charging_power: float = float(dc_system[2])
                    generation_power: float = float(dc_system[3])
                    res.append(BusChargingDcCoupling(charging_power, generation_power))
                elif dc_type == BusChargingProfileDcCoupling.__name__:
                    capacity: float = float(dc_system[2])
                    file_name: str = dc_system[3]
                    file: str = os.path.join(self.__profile_config.technical_profile_dir, file_name)
                    res.append(BusChargingProfileDcCoupling(self.__general_config, capacity,  file))
                elif dc_type == USPDCCoupling.__name__:
                    file_name: str = dc_system[2]
                    res.append(USPDCCoupling(self.__general_config, self.__profile_config, file_name))
                else:
                    options: [str] = list()
                    options.append(NoDcCoupling.__name__)
                    options.append(BusChargingDcCoupling.__name__)
                    raise Exception('DcCoupling ' + dc_type + ' is unknown. '
                                                              'Following options are available: ' + str(options))
        return res

    def create_storage_systems_dc(self, name: str, data_export: DataHandler,
                                  ambient_thermal_model: AmbientThermalModel,
                                  intermediate_circuit_voltage: float, system_id: int) -> [StorageSystemDC]:
        dc_systems: [[str]] = self.__system_config.storage_systems_dc
        res: [StorageSystemDC] = list()
        storage_id = 0
        for dc_system in dc_systems:
            try:
                system = dc_system[StorageSystemConfig.DC_SYSTEM_NAME]
                dc_type: str = dc_system[StorageSystemConfig.DC_SYSTEM_CONVERTER]
                converter_configuration: dict = self.__system_config.dcdc_converter
                dc_converter: str = converter_configuration[dc_type][StorageSystemConfig.DCDC_CONVERTER_TYPE]
                if system == name and DcDcConverter.__name__ in dc_converter:
                    storage_id += 1
                    technology: str = dc_system[StorageSystemConfig.DC_SYSTEM_STORAGE]
                    dcdc_converter: DcDcConverter = self.create_dcdc_converter(dc_type, intermediate_circuit_voltage)
                    storage_technology: StorageTechnology = self.create_storage_technology(technology, data_export,
                                                                                           ambient_thermal_model,
                                                                                           storage_id, system_id,
                                                                                           intermediate_circuit_voltage)
                    res.append(StorageSystemDC(system_id, storage_id, data_export, dcdc_converter, storage_technology))
            except IndexError:
                pass
            except KeyError:
                pass
        if not res:
            raise Exception('Storage system ' + name + ' has no storage data. Please specify your storage system.')
        return res

    def create_storage_technology(self, technology: str, data_export: DataHandler,
                                  ambient_thermal_model: AmbientThermalModel,
                                  storage_id: int, system_id: int, voltage: float) -> [StorageTechnology]:
        technology_configuration: dict = self.__system_config.storage_technologies
        technology_set: list = technology_configuration[technology]
        capacity: float = float(technology_set[StorageSystemConfig.STORAGE_CAPACITY])
        technology: str = technology_set[StorageSystemConfig.STORAGE_TECHNOLOGY]
        if technology == self.__lithium_ion_name:
            self.__log.debug('Creating ' + technology + ' as storage system id ' + str(storage_id))
            cell: str = technology_set[StorageSystemConfig.BATTERY_CELL]
            try:
                soh: float = float(technology_set[StorageSystemConfig.BATTERY_SOH])
            except IndexError:
                soh: float = self.__config_battery.start_soh
            return LithiumIonBattery(cell, voltage, capacity, soh, data_export,
                                     ambient_thermal_model, storage_id, system_id,
                                     self.__simulation_config)
        elif technology == self.__redox_flow_name:
            self.__log.debug('Creating ' + technology + ' as storage system id ' + str(storage_id))
            stack_type = technology_set[StorageSystemConfig.REDOX_FLOW_STACK]
            stack_module_power: float = float(technology_set[StorageSystemConfig.STACK_MODULE_POWER])
            try:
                pump_algorithm = technology_set[StorageSystemConfig.REDOX_FLOW_PUMP_ALGORITHM]
            except IndexError:
                pump_algorithm = 'Default'
            return RedoxFlow(stack_type, stack_module_power, voltage, capacity, pump_algorithm, data_export, storage_id,
                             system_id, self.__simulation_config)
        elif technology == self.__hydrogen_name:
            self.__log.debug('Creating ' + technology + ' as storage system id ' + str(storage_id))
            # fuel_cell = technology_set[2]
            # fuel_cell_nominal_power = float(technology_set[3])
            # fuel_cell_thermal_model = technology_set[4]
            # fuel_cell_pressure_model = technology_set[5]
            # electrolyzer = technology_set[6]
            # electrolyzer_nominal_power = float(technology_set[7])
            # electrolyzer_thermal_model = technology_set[8]
            # electrolyzer_pressure_model = technology_set[9]
            # storage = technology_set[10]
            # max_pressure = float(technology_set[11])
            fuel_cell = technology_set[StorageSystemConfig.FUEL_CELL_TYPE]
            fuel_cell_nominal_power = float(technology_set[StorageSystemConfig.FUEL_CELL_POWER])
            electrolyzer = technology_set[StorageSystemConfig.ELECTROLYZER_TYPE]
            electrolyzer_nominal_power = float(technology_set[StorageSystemConfig.ELECTROLYZER_POWER])
            storage = technology_set[StorageSystemConfig.HYDROGEN_STORAGE]
            max_pressure = float(technology_set[StorageSystemConfig.HYDROGEN_TANK_PRESSURE])
            return Hydrogen(data_export, fuel_cell, fuel_cell_nominal_power, electrolyzer, electrolyzer_nominal_power,
                            storage, capacity, max_pressure, ambient_thermal_model, system_id, storage_id,
                            self.__simulation_config)
        else:
            options: [str] = list()
            options.append(self.__lithium_ion_name)
            options.append(self.__redox_flow_name)
            options.append(self.__hydrogen_name)
            raise Exception('Storage technology ' + technology + ' is unknown. '
                                                                 'Following options are available: ' + str(options))

    def close(self):
        self.__log.close()
