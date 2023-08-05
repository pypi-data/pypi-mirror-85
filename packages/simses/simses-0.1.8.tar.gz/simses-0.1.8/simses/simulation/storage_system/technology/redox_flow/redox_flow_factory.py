from configparser import ConfigParser

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.config.data.auxiliary_data_config import AuxiliaryDataConfig
from simses.config.data.redox_flow_data_config import RedoxFlowDataConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.redox_flow_config import RedoxFlowConfig
from simses.simulation.storage_system.auxiliary.pump.fixeta_centrifugal_pump import FixEtaCentrifugalPump
from simses.simulation.storage_system.auxiliary.pump.pump import Pump
from simses.simulation.storage_system.auxiliary.pump.scalable_variable_eta_centrifugal_pump import \
    ScalableVariableEtaCentrifugalPump
from simses.simulation.storage_system.auxiliary.pump.variable_eta_centrifugal_pump import VariableEtaCentrifugalPump
from simses.simulation.storage_system.technology.redox_flow.degradation_model.const_hydrogen_current import \
    ConstHydrogenCurrent
from simses.simulation.storage_system.technology.redox_flow.degradation_model.no_degradation_model import NoDegradation
from simses.simulation.storage_system.technology.redox_flow.degradation_model.variable_hydrogen_current import \
    VariableHydrogenCurrent
from simses.simulation.storage_system.technology.redox_flow.electrochemical_model.control_system.control_system import \
    RedoxControlSystem
from simses.simulation.storage_system.technology.redox_flow.electrochemical_model.electrochemical_model import \
    ElectrochemicalModel
from simses.simulation.storage_system.technology.redox_flow.electrochemical_model.rint_model import RintModel

from simses.simulation.storage_system.technology.redox_flow.pump_algorithm.fix_flow_rate_start_stop import \
    FixFlowRateStartStop
from simses.simulation.storage_system.technology.redox_flow.pump_algorithm.pump_algorithm import PumpAlgorithm
from simses.simulation.storage_system.technology.redox_flow.pump_algorithm.stoich_flow_rate import StoichFlowRate
from simses.simulation.storage_system.technology.redox_flow.stack_module.cell_data_stack_5600w import CellDataStack5600W
from simses.simulation.storage_system.technology.redox_flow.stack_module.electrolyte_system.electrolyte_system import \
    ElectrolyteSystem
from simses.simulation.storage_system.technology.redox_flow.stack_module.electrolyte_system.vanadium_system_ import \
    VanadiumSystem
from simses.simulation.storage_system.technology.redox_flow.stack_module.dummy_stack_3000w import \
    DummyStack3000W
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class RedoxFlowFactory:

    def __init__(self, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__config_general: GeneralSimulationConfig = GeneralSimulationConfig(config)
        self.__config_redox_flow: RedoxFlowConfig = RedoxFlowConfig(config)
        self.__config_redox_flow_data: RedoxFlowDataConfig = RedoxFlowDataConfig()
        self.__config_auxiliary_data: AuxiliaryDataConfig = AuxiliaryDataConfig()

    def create_redox_flow_state_from(self, storage_id: int, system_id: int, stack_module: StackModule,
                                     capacity: float, redox_flow_state: RedoxFlowState = None):
        """
        Initial creates the RedoxFlowState object if it doesn't exist.

        Parameters
        ----------
        storage_id : int
            storage id
        system_id : int
            system id
        stack_module : StackModule
            stack module based on specific stack typ
        capacity : float
            Capacity of the electrolyte of the redox flow battery in Wh.
        redox_flow_state : RedoxFlowState

        Returns
        -------
        RedoxFlowState
            state of the redox flow battery
        """
        if redox_flow_state is None:
            time: float = self.__config_general.start
            soc: float = self.__config_redox_flow.soc
            rfbs = RedoxFlowState(system_id, storage_id)
            rfbs.time = time
            rfbs.soc = soc
            rfbs.soc_stack = soc
            rfbs.voltage = stack_module.get_open_circuit_voltage(rfbs)
            rfbs.open_circuit_voltage = stack_module.get_open_circuit_voltage(rfbs)
            rfbs.capacity = capacity
            rfbs.soh = 1.0
            rfbs.time_pump = 0
            rfbs.internal_resistance = stack_module.get_internal_resistance(rfbs)
            rfbs.power = 0.0
            rfbs.power_in = 0.0
            rfbs.power_loss = 0.0
            rfbs.pressure_loss = 0.0
            rfbs.pressure_drop_anolyte = 0.0
            rfbs.pressure_drop_catholyte = 0.0
            rfbs.flow_rate_anolyte = 0.0
            rfbs.flow_rate_catholyte = 0.0
            rfbs.fulfillment = 1.0
            rfbs.electrolyte_temperature = 303.15

            return rfbs
        else:
            return redox_flow_state

    def create_stack_module(self, stack_module: str, electrolyte_system: ElectrolyteSystem,
                            voltage: float, power: float) -> StackModule:
        """
        Initial creates the StackModule object for a specific stack typ.

        Parameters
        ----------
        stack_module : str
            stack type for stack module
        electrolyte_system : ElectrolyteSystem
            electrolyte system
        voltage : float
            nominal stack module voltage in V of the redox flow battery
        power : float
            nominal stack module power in W of the redox flow battery

        Returns
        -------
        StackModule
        """
        if stack_module == CellDataStack5600W.__name__:
            self.__log.debug('Creating stack module as ' + stack_module)
            return CellDataStack5600W(electrolyte_system, voltage, power, self.__config_redox_flow_data,
                                      self.__config_redox_flow)
        elif stack_module == DummyStack3000W.__name__:
            self.__log.debug('Creating stack module as ' + stack_module)
            return DummyStack3000W(electrolyte_system, voltage, power, self.__config_redox_flow)

        else:
            options: [str] = list()
            options.append(CellDataStack5600W.__name__)
            options.append(DummyStack3000W.__name__)

            raise Exception('Specified stack module ' + stack_module + ' is unknown. '
                                                                       'Following options are available: ' + str(
                options))

    def check_pump_algorithm(self, pump_algorithm: str, stack_module) -> str:
        if pump_algorithm == 'Default':
            if stack_module == CellDataStack5600W.__name__ or stack_module == DummyStack3000W.__name__:
                return 'StoichFlowRate'
        else:
            return pump_algorithm

    def create_pumps(self, pump_algorithm: str) -> Pump:
        if pump_algorithm == FixFlowRateStartStop.__name__:
            pump_type = 'FixEtaCentrifugalPump'
            self.__log.debug('Creating pumps as ' + pump_type)
            efficiency: float = 0.3
            return FixEtaCentrifugalPump(efficiency)
        # select if a special pump with a data file should be used
        # elif pump_algorithm == ConstantPressurePulsed.__name__:
        #     pump_type = 'VariableEtaCentrifugalPump'
        #     self.__log.debug('Creating pumps as ' + pump_type)
        #     return VariableEtaCentrifugalPump(self.__config_auxiliary_data)
        elif pump_algorithm == StoichFlowRate.__name__ or pump_algorithm == ConstantPressurePulsed.__name__:
            pump_type = 'ScalableVariableEtaCentrifugalPump'
            self.__log.debug('Creating pumps as ' + pump_type)
            return ScalableVariableEtaCentrifugalPump()
        else:
            options: [str] = list()
            options.append(StoichFlowRate.__name__)
            options.append(FixFlowRateStartStop.__name__)
            raise Exception('Specified pump algorithm ' + pump_algorithm + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_electrolyte_system(self, capacity: float, stack_type: str):
        """
        Initial creates the ElectrolyteSystem object.

        Parameters
        ----------
        capacity : float
            Total start capacity of the redox flow system in Wh.
        stack_type: str
            stack type of the redox flow battery

        Returns
        -------
        ElectrolyteSystem
        """
        if (stack_type == CellDataStack5600W.__name__ or stack_type == DummyStack3000W.__name__):
            self.__log.debug('Creating electrolyte system as VanadiumSystem')
            return VanadiumSystem(capacity, self.__config_redox_flow)
        else:
            options: [str] = list()
            options.append(CellDataStack5600W.__name__)
            options.append(DummyStack3000W.__name__)
            raise Exception('Specified stack module for vanadium system ' + stack_type + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_electrochemical_model(self, stack_module: StackModule,
                                     battery_management_system: RedoxControlSystem
                                     , electrolyte_system: ElectrolyteSystem,
                                     electrochemical_model: ElectrochemicalModel = None) -> ElectrochemicalModel:
        """
        Initial creates the ElectrochemicalModel object for a specific model, which includes the battery management
        system requests.

        Parameters
        ----------
        stack_module : StackModule
            stack module of a redox flow battery
        battery_management_system : RedoxControlSystem
            battery management system of the redox flow battery
        electrolyte_system: ElectrolyteSystem
            electrolyte system of the redox flow battery
        electrochemical_model : ElectrochemicalModel
            electrochemical model of the redox flow battery

        Returns
        -------
            ElectrochemicalModel
        """
        if electrochemical_model is None:
            self.__log.debug('Creating electrochemical model for redox flow system depended on stack module ' +
                             stack_module.__class__.__name__)
            return RintModel(stack_module, battery_management_system, electrolyte_system)
        else:
            return electrochemical_model

    def create_redox_management_system(self, stack_module: StackModule, electrolyte_system: ElectrolyteSystem,
                                       pump_algorithm: PumpAlgorithm,
                                       redox_management_system: RedoxControlSystem = None) \
            -> RedoxControlSystem:
        """
        Initial creates the BatteryManagementSystem object of the redox flow battery.

        Parameters
        ----------
        stack_module : StackModule
            stack module of a redox flow battery
        electrolyte_system : ElectrolyteSystem
            management system of a redox flow battery
        pump_algorithm : PumpAlgorithm
            pump algorithm of the redox flow battery
        redox_management_system : RedoxControlSystem
            battery management system of the redox flow battery

        Returns
        -------
            RedoxControlSystem
        """
        if redox_management_system is None:
            self.__log.debug('Creating battery management system for redox flow system depended on stack module '
                             + stack_module.__class__.__name__)
            return RedoxControlSystem(stack_module, electrolyte_system, pump_algorithm, self.__config_redox_flow)
        else:
            return redox_management_system

    def create_degradation_model(self, stack_module: StackModule):
        # Degradation model can be changed here.
        degradation_model = 'ConstHydrogenCurrent'
        if degradation_model == 'NoDegradation':
            self.__log.debug('Creating degradation Model as ' + degradation_model)
            return NoDegradation()
        elif degradation_model == 'ConstHydrogenCurrent':
            self.__log.debug('Creating degradation Model as ' + degradation_model)
            return ConstHydrogenCurrent(stack_module)
        elif degradation_model == 'VariableHydrogenCurrent':
            self.__log.debug('Creating degradation Model as ' + degradation_model)
            return VariableHydrogenCurrent(stack_module, self.__config_redox_flow_data)
        else:
            options: [str] = list()
            options.append(NoDegradation.__name__)
            options.append(ConstHydrogenCurrent.__name__)
            options.append(VariableHydrogenCurrent.__name__)
            raise Exception('Specified degradation model ' + degradation_model + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_pump_algorithm(self, pump: Pump, stack_module: StackModule, electrolyte_system: ElectrolyteSystem,
                              pump_algorithm: str):
        if pump_algorithm == StoichFlowRate.__name__:
            self.__log.debug('Creating pump algorithm as ' + pump_algorithm)
            return StoichFlowRate(stack_module, pump, electrolyte_system, self.__config_redox_flow)
        elif pump_algorithm == FixFlowRateStartStop.__name__:
            self.__log.debug('Creating pump algorithm as ' + pump_algorithm)
            return FixFlowRateStartStop(stack_module, pump, electrolyte_system)
        else:
            options: [str] = list()
            options.append(StoichFlowRate.__name__)
            options.append(FixFlowRateStartStop.__name__)
            raise Exception('Specified pump algorithm ' + pump_algorithm + ' is unknown. '
                            'Following options are available: ' + str(options))

    def close(self):
        self.__log.close()
