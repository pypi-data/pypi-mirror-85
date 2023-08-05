from configparser import ConfigParser

from simses.analysis.data.data import Data
from simses.analysis.data.electrolyzer_data import ElectrolyzerData
from simses.analysis.data.energy_management_data import EnergyManagementData
from simses.analysis.data.fuel_cell_data import FuelCellData
from simses.analysis.data.lithium_ion_data import LithiumIonData
from simses.analysis.data.redox_flow_data import RedoxFlowData
from simses.analysis.data.system_data import SystemData
from simses.analysis.evaluation.ecologic.ecologic_evaluation import EcologicEvaluation
from simses.analysis.evaluation.economic.economic_evaluation import EconomicEvaluation
from simses.analysis.evaluation.economic.revenue_stream.demand_charge_reduction import DemandChargeReduction
from simses.analysis.evaluation.economic.revenue_stream.electricity_consumption_revenue_stream import \
    ElectricityConsumptionRevenueStream
from simses.analysis.evaluation.economic.revenue_stream.fcr_revenue_stream import FCRRevenue
from simses.analysis.evaluation.economic.revenue_stream.intraday_recharge_revenue_stream import IntradayRechargeRevenue
from simses.analysis.evaluation.economic.revenue_stream.operation_and_maintenance_revenue_stream import \
    OperationAndMaintenanceRevenue
from simses.analysis.evaluation.economic.revenue_stream.revenue_stream import RevenueStream
from simses.analysis.evaluation.economic.revenue_stream.self_consumption_increase import SelfConsumptionIncrease
from simses.analysis.evaluation.evaluation import Evaluation
from simses.analysis.evaluation.evaluation_merger import EvaluationMerger
from simses.analysis.evaluation.technical.electrolyzer_evaluation import ElectrolyzerTechnicalEvaluation
from simses.analysis.evaluation.technical.fuel_cell_evaluation import FuelCellTechnicalEvaluation
from simses.analysis.evaluation.technical.lithium_ion_evaluation import LithiumIonTechnicalEvaluation
from simses.analysis.evaluation.technical.redox_flow_evaluation import RedoxFlowTechnicalEvaluation
from simses.analysis.evaluation.technical.site_level_evaluation import SiteLevelEvaluation
from simses.analysis.evaluation.technical.system_evaluation import SystemTechnicalEvaluation
from simses.commons.log import Logger
from simses.commons.profile.economic_profile.fcr_market_profile import FcrMarketProfile
from simses.commons.profile.economic_profile.intraday_market_profile import IntradayMarketProfile
from simses.config.analysis.economic_analysis_config import EconomicAnalysisConfig
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig
from simses.config.analysis.market_profile_config import MarketProfileConfig
from simses.config.simulation.battery_config import BatteryConfig
from simses.config.simulation.energy_management_config import EnergyManagementConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.storage_system_config import StorageSystemConfig
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.frequency_containment_reserve import \
    FrequencyContainmentReserve
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.intraday_market_recharge import \
    IntradayMarketRecharge
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.peak_shaving_perfect_foresight import \
    PeakShavingPerfectForesight
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.peak_shaving_simple import \
    SimplePeakShaving
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.residential_pv_feed_in_damp import \
    ResidentialPvFeedInDamp
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.residential_pv_greedy import \
    ResidentialPvGreedy
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.use_all_renewable_energy import \
    UseAllRenewableEnergy
from simses.simulation.energy_management.operation_strategy.stacked_operation_strategy.fcr_idm_recharge_stacked import \
    FcrIdmRechargeStacked


class AnalysisFactory:

    # TODO Is the dependence of simulation pkg acceptable? --> MM
    __SELF_CONSUMPTION_INCREASE: [str] = [ResidentialPvGreedy.__name__, ResidentialPvFeedInDamp.__name__,
                                          SimplePeakShaving.__name__, PeakShavingPerfectForesight.__name__]
    __DEMAND_CHARGE_REDUCTION: [str] = [SimplePeakShaving.__name__, PeakShavingPerfectForesight.__name__]
    __FREQUENCY_CONTAINMENT_RESERVE: [str] = [FrequencyContainmentReserve.__name__, FcrIdmRechargeStacked.__name__]
    __INTRADAY_MARKET: [str] = [FcrIdmRechargeStacked.__name__, IntradayMarketRecharge.__name__]
    __ELECTRICITY_CONSUMPTION_REVENUE_STREAM: [str] = [UseAllRenewableEnergy.__name__]

    def __init__(self, path: str, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__result_path: str = path
        self.__analysis_config: GeneralAnalysisConfig = GeneralAnalysisConfig(config)
        self.__economic_analysis_config: EconomicAnalysisConfig = EconomicAnalysisConfig(config)
        self.__market_profile_config: MarketProfileConfig = MarketProfileConfig(config)
        self.__simulation_config: GeneralSimulationConfig = GeneralSimulationConfig(config=None, path=self.__result_path)
        self.__battery_config: BatteryConfig = BatteryConfig(config=None, path=self.__result_path)
        self.__energy_management_config: EnergyManagementConfig = EnergyManagementConfig(config=None, path=self.__result_path)
        self.__storage_system_config: StorageSystemConfig = StorageSystemConfig(config=None, path=self.__result_path)
        self.__do_plotting: bool = self.__analysis_config.plotting
        self.__do_system_analysis: bool = self.__analysis_config.system_analysis
        self.__do_lithium_ion_analysis: bool = self.__analysis_config.lithium_ion_analysis
        self.__do_redox_flow_analysis: bool = self.__analysis_config.redox_flow_analysis
        self.__do_hydrogen_analysis: bool = self.__analysis_config.hydrogen_analysis
        self.__do_site_level_analysis: bool = self.__analysis_config.site_level_analysis
        self.__do_economic_analysis: bool = self.__analysis_config.economical_analysis
        try:
            self.__energy_management_data: EnergyManagementData = EnergyManagementData.get_system_data(self.__result_path, self.__simulation_config)[0]
        except IndexError:
            self.__log.warn('No energy management data found!')
            self.__energy_management_data = None

    def __create_data_list(self) -> [Data]:
        config = self.__simulation_config
        path = self.__result_path
        data_list: [Data] = list()
        data_list.extend(LithiumIonData.get_system_data(path, config))
        data_list.extend(RedoxFlowData.get_system_data(path, config))
        data_list.extend(SystemData.get_system_data(path, config))
        # data_list.extend(HydrogenData.get_system_data(path, config))
        data_list.extend(ElectrolyzerData.get_system_data(path, config))
        data_list.extend(FuelCellData.get_system_data(path, config))
        for data in data_list:
            self.__log.info('Created ' + type(data).__name__)
        return data_list

    def __create_revenue_streams(self, system_data) -> [RevenueStream]:
        revenue_streams: [RevenueStream] = list()
        economic_config: EconomicAnalysisConfig = self.__economic_analysis_config
        energy_management_strategy: str = self.__energy_management_config.operation_strategy
        if self.__energy_management_data is None:
            self.__log.warn('No energy management data available ----> No economic evaluation possible!')
            return revenue_streams
        if energy_management_strategy in self.__SELF_CONSUMPTION_INCREASE:
            revenue_streams.append(SelfConsumptionIncrease(self.__energy_management_data, system_data, economic_config))
            self.__log.info('Adding ' + SelfConsumptionIncrease.__name__ + ' to revenue streams')
        if energy_management_strategy in self.__DEMAND_CHARGE_REDUCTION:
            revenue_streams.append(DemandChargeReduction(self.__energy_management_data, system_data, economic_config))
            self.__log.info('Adding ' + DemandChargeReduction.__name__ + ' to revenue streams')
        if energy_management_strategy in self.__FREQUENCY_CONTAINMENT_RESERVE:
            market: FcrMarketProfile = FcrMarketProfile(self.__simulation_config, self.__market_profile_config)
            revenue_streams.append(FCRRevenue(self.__energy_management_data, system_data, economic_config, market,
                                              self.__simulation_config))
            self.__log.info('Adding ' + FCRRevenue.__name__ + ' to revenue streams')
        if energy_management_strategy in self.__INTRADAY_MARKET:
            market: IntradayMarketProfile = IntradayMarketProfile(self.__simulation_config, self.__market_profile_config)
            revenue_streams.append(IntradayRechargeRevenue(self.__energy_management_data, system_data, economic_config,
                                                           market, self.__simulation_config))
            self.__log.info('Adding ' + IntradayRechargeRevenue.__name__ + ' to revenue streams')
        if energy_management_strategy in self.__ELECTRICITY_CONSUMPTION_REVENUE_STREAM:
            revenue_streams.append(ElectricityConsumptionRevenueStream(self.__energy_management_data, system_data, economic_config))
            self.__log.info('Adding ' + ElectricityConsumptionRevenueStream.__name__ + ' to revenue streams')
        if not revenue_streams:
            self.__log.warn('No revenue streams are defined for chosen Energy Management Strategy: ' + energy_management_strategy)
        revenue_streams.append(OperationAndMaintenanceRevenue(self.__energy_management_data, system_data, economic_config))
        self.__log.info('Adding ' + OperationAndMaintenanceRevenue.__name__ + ' to revenue streams')
        return revenue_streams

    def create_evaluations(self) -> [Evaluation]:
        data_list: [Data] = self.__create_data_list()
        evaluations: [Evaluation] = list()
        config: GeneralAnalysisConfig = self.__analysis_config
        ems_config: EnergyManagementConfig = self.__energy_management_config
        path: str = self.__result_path
        for data in data_list:
            if isinstance(data, SystemData):
                if self.__do_system_analysis:
                    evaluations.append(SystemTechnicalEvaluation(data, config, self.__storage_system_config, path))
                    evaluations.append(EcologicEvaluation(data, config))
                if data.is_top_level_system and self.__energy_management_data is not None:
                    if self.__do_site_level_analysis:
                        evaluations.append(SiteLevelEvaluation(data, self.__energy_management_data, config, ems_config, path))
                    if self.__do_economic_analysis:
                        revenue_streams = self.__create_revenue_streams(data)
                        evaluations.append(EconomicEvaluation(data, self.__economic_analysis_config, revenue_streams, config, self.__storage_system_config))
            elif isinstance(data, LithiumIonData) and self.__do_lithium_ion_analysis:
                evaluations.append(LithiumIonTechnicalEvaluation(data, config, self.__battery_config, path))
            elif isinstance(data, RedoxFlowData) and self.__do_redox_flow_analysis:
                evaluations.append(RedoxFlowTechnicalEvaluation(data, config, path))
            # elif isinstance(data, HydrogenData) and self.__do_hydrogen_analysis:
            #     evaluations.append(HydrogenTechnicalEvaluation(data, config, path))
            elif isinstance(data, ElectrolyzerData) and self.__do_hydrogen_analysis:
                evaluations.append(ElectrolyzerTechnicalEvaluation(data, config, path))
            elif isinstance(data, FuelCellData) and self.__do_hydrogen_analysis:
                evaluations.append(FuelCellTechnicalEvaluation(data, config, path))
        return evaluations

    def create_evaluation_merger(self) -> EvaluationMerger:
        return EvaluationMerger(self.__result_path, self.__analysis_config)

    def close(self):
        self.__log.close()
        # TODO close Data but not for all instances
        # Data.close()
