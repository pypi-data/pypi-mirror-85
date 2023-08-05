from simses.analysis.data.data import Data
from simses.analysis.evaluation.evaluation import Evaluation
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig


class EcologicEvaluation(Evaluation):

    def __init__(self, data: Data, config: GeneralAnalysisConfig):
        super().__init__(data, config, config.environmental_analysis)

    def evaluate(self):
        pass

    def plot(self) -> None:
        pass

    def co2_footprint(self):
        pass

    def close(self) -> None:
        pass
