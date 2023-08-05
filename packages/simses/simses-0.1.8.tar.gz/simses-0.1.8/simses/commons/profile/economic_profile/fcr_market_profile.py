from simses.commons.profile.economic_profile.market_profile import MarketProfile
from simses.commons.profile.file_profile import FileProfile
from simses.commons.timeseries.interpolation.last_value import LastValue
from simses.config.analysis.market_profile_config import MarketProfileConfig
from simses.config.simulation.general_config import GeneralSimulationConfig


class FcrMarketProfile(MarketProfile):
    """
    Provides the FCR market prices
    """
    def __init__(self, general_config: GeneralSimulationConfig, config: MarketProfileConfig):
        super().__init__()
        self.__file: FileProfile = FileProfile(general_config, config.fcr_price_file, interpolation=LastValue())

    def next(self, time: float) -> float:
        return self.__file.next(time)

    def initialize_profile(self):
        return self.__file.initialize_file()

    def profile_data_to_list(self, sign_factor=1) -> ([float], [float]):
        time, values = self.__file.profile_data_to_list(sign_factor)
        return time, values

    def close(self):
        self.__file.close()



