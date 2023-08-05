from configparser import ConfigParser

from simses.config.analysis.analysis_config import AnalysisConfig
from simses.constants_simses import ROOT_PATH


class MarketProfileConfig(AnalysisConfig):
    """
    Market profile configs
    """

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        # self.__log: Logger = Logger(type(self).__name__)
        self.__section: str = 'MARKET_PROFILE'

    @property
    def market_profile_dir(self) -> str:
        """Returns directory of market profiles from __analysis_config file_name"""
        return ROOT_PATH + self.get_property(self.__section, 'MARKET_PROFILE_DIR')

    @property
    def fcr_price_file(self) -> str:
        """Returns soc profile file_name name from __analysis_config file_name"""
        return self.market_profile_dir + self.get_property(self.__section, 'FCR_PRICE_PROFILE')

    @property
    def intraday_price_file(self) -> str:
        """ Return PV generation profile file_name name from __analysis_config file_name"""
        return self.market_profile_dir + self.get_property(self.__section, 'INTRADAY_PRICE_PROFILE')

