from simses.config.data.data_config import DataConfig
from simses.constants_simses import ROOT_PATH


class AuxiliaryDataConfig(DataConfig):

    def __init__(self, path: str = None):
        super().__init__(path)
        self.__section: str = 'AUXILIARY_DATA'

    @property
    def auxiliary_pump_data_dir(self) -> str:
        """Returns directory of pump data files"""
        return ROOT_PATH + self.get_property(self.__section, 'AUXILIARY_PUMP_DATA_DIR')

    @property
    def pump_eta_file(self) -> str:
        """Returns filename for efficiency file of chosen pump"""
        return self.auxiliary_pump_data_dir + self.get_property(self.__section, 'PUMP_ETA_FILE')
