import os
from configparser import ConfigParser

from simses.config.analysis.analysis_config import AnalysisConfig


class GeneralAnalysisConfig(AnalysisConfig):
    """
    General analysis configs
    """

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        self.__section: str = 'GENERAL'

    def get_result_for(self, path: str) -> str:
        """Returns name of the simulation to analyse."""
        __simulation = self.get_property(self.__section, 'SIMULATION')
        if __simulation == 'LATEST':
            result_dirs = list()
            tmp_dirs = os.listdir(path)
            # res = filter(os.path.isdir, tmp_dirs)
            for dir in tmp_dirs:
                if os.path.isdir(path + dir):
                    result_dirs.append(path + dir + '/')
            return max(result_dirs, key=os.path.getmtime)
        else:
            return path + __simulation + '/'

    @property
    def system_analysis(self) -> bool:
        """Returns boolean value for system_analysis after the simulation"""
        return self.get_property(self.__section, 'SYSTEM_ANALYSIS') in ['True']

    @property
    def lithium_ion_analysis(self) -> bool:
        """Returns boolean value for lithium_ion_analysis after the simulation"""
        return self.get_property(self.__section, 'LITHIUM_ION_ANALYSIS') in ['True']

    @property
    def redox_flow_analysis(self) -> bool:
        """Returns boolean value for redox_flow_analysis after the simulation"""
        return self.get_property(self.__section, 'REDOX_FLOW_ANALYSIS') in ['True']

    @property
    def hydrogen_analysis(self) -> bool:
        """Returns boolean value for redox_flow_analysis after the simulation"""
        return self.get_property(self.__section, 'HYDROGEN_ANALYSIS') in ['True']

    @property
    def site_level_analysis(self) -> bool:
        """Returns boolean value for redox_flow_analysis after the simulation"""
        return self.get_property(self.__section, 'SITE_LEVEL_ANALYSIS') in ['True']

    @property
    def plotting(self) -> bool:
        """Returns boolean value for matplot_plotting after the simulation"""
        return self.get_property(self.__section, 'PLOTTING') in ['True']

    @property
    def technical_analysis(self) -> bool:
        """Returns boolean value for technical analysis directly after the simulation"""
        return self.get_property(self.__section, 'TECHNICAL_ANALYSIS') in ['True']

    @property
    def economical_analysis(self) -> bool:
        """Returns boolean value for economical analysis directly after the simulation"""
        return self.get_property(self.__section, 'ECONOMICAL_ANALYSIS') in ['True']

    @property
    def environmental_analysis(self) -> bool:
        """Returns boolean value for environmental analysis directly after the simulation"""
        return self.get_property(self.__section, 'ENVIRONMENTAL_ANALYSIS') in ['True']

    @property
    def export_analysis_to_csv(self) -> bool:
        """Defines if analysis results are to be exported to csv files"""
        return self.get_property(self.__section, 'EXPORT_ANALYSIS_TO_CSV') in ['True']

    @property
    def print_result_to_console(self) -> bool:
        """Defines if analysis results are to be printed to console"""
        return self.get_property(self.__section, 'PRINT_RESULTS_TO_CONSOLE') in ['True']

    @property
    def export_analysis_to_batch(self) -> bool:
        """Defines if analysis results are written to batch files"""
        return self.get_property(self.__section, 'EXPORT_ANALYSIS_TO_BATCH') in ['True']

    @property
    def merge_analysis(self) -> bool:
        """Defines if analysis results are merged"""
        return self.get_property(self.__section, 'MERGE_ANALYSIS') in ['True']
