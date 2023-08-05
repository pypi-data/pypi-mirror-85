from simses.commons.profile.file_profile import FileProfile
from simses.commons.profile.technical_profile.technical_profile import TechnicalProfile
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig


class SocProfile(TechnicalProfile):

    def __init__(self, config: GeneralSimulationConfig, profile_config: ProfileConfig, delimiter=','):
        super().__init__()
        self.__file: FileProfile = FileProfile(config, profile_config.soc_file, delimiter=delimiter,
                                               value_index=profile_config.soc_file_value)

    def next(self, time: float) -> float:
        return self.__file.next(time)

    def close(self):
        self.__file.close()
