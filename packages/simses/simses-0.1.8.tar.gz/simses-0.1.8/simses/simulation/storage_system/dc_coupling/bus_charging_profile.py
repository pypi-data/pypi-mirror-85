from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.dc_coupling.dc_coupling import DcCoupling
from simses.simulation.storage_system.dc_coupling.generation.no_dc_generation import NoDcGeneration
from simses.simulation.storage_system.dc_coupling.load.dc_bus_charging_profile import DcBusChargingProfile


class BusChargingProfileDcCoupling(DcCoupling):

    def __init__(self, config: GeneralSimulationConfig, capacity: float, file_name: str):
        super().__init__(DcBusChargingProfile(config, capacity, file_name), NoDcGeneration())
