from simses.config.data.electrolyzer_data_config import ElectrolyzerDataConfig
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.pem_electrolyzer_multi_dim_analytic_model.pem_electrolyzer_model import \
    PemElectrolyzerMultiDimAnalytic


class PemElectrolyzerMultiDimAnalyticPtlCoating(PemElectrolyzerMultiDimAnalytic):
    """ PEM Electrolyzer with Pt-coated Ti-PTL at anode site, which prevents the cyclic increase of its resistance """
    def __init__(self, electrolyzer_maximal_power: float, electrolyzer_data_config: ElectrolyzerDataConfig):
        super().__init__(electrolyzer_maximal_power, electrolyzer_data_config)
