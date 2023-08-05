from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig
from simses.simulation.storage_system.dc_coupling.dc_coupling import DcCoupling
from simses.simulation.storage_system.dc_coupling.generation.no_dc_generation import NoDcGeneration
from simses.simulation.storage_system.dc_coupling.load.dc_usv_load import RadioUPSLoad


class USPDCCoupling(DcCoupling):

    def __init__(self, config: GeneralSimulationConfig, profile_config: ProfileConfig, file_name: str):
        super(USPDCCoupling, self).__init__(RadioUPSLoad(config, profile_config, file_name), NoDcGeneration())
