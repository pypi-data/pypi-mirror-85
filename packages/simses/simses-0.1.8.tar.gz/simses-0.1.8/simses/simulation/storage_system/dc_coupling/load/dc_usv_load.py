from simses.commons.profile.file_profile import FileProfile
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.dc_coupling.load.dc_load import DcLoad


class RadioUPSLoad(DcLoad):

    def __init__(self, config: GeneralSimulationConfig, profile_config: ProfileConfig, file_name: str):
        super().__init__()
        self.__profile: FileProfile = FileProfile(config, profile_config.power_profile_dir + file_name)
        self.__power: float = 0.0

    def get_power(self) -> float:
        return self.__power

    def calculate_power(self, time: float) -> None:
        value: float = self.__profile.next(time)
        # tbd
        self.__power = value

    def get_auxiliaries(self) -> [Auxiliary]:
        pass

    def close(self) -> None:
        self.__profile.close()
