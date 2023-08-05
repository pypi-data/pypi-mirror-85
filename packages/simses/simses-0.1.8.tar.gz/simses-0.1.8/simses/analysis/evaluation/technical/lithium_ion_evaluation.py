from simses.analysis.data.lithium_ion_data import LithiumIonData
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Description, Unit
from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotly_plotting import PlotlyPlotting
from simses.analysis.evaluation.plotting.plotting import Plotting
from simses.analysis.evaluation.technical.technical_evaluation import TechnicalEvaluation
from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig
from simses.config.simulation.battery_config import BatteryConfig


class LithiumIonTechnicalEvaluation(TechnicalEvaluation):

    title = 'Results'

    def __init__(self, data: LithiumIonData, config: GeneralAnalysisConfig, battery_config: BatteryConfig, path: str):
        super().__init__(data, config)
        title_extension: str = ' for system ' + self.get_data().id
        self.title += title_extension
        self.__result_path = path

    def evaluate(self):
        super().evaluate()
        self.append_result(EvaluationResult(Description.Technical.EQUIVALENT_FULL_CYCLES, Unit.NONE, self.equivalent_full_cycles))
        self.append_result(EvaluationResult(Description.Technical.DEPTH_OF_DISCHARGE, Unit.PERCENTAGE, self.depth_of_discharges))
        self.append_result(EvaluationResult(Description.Technical.ENERGY_THROUGHPUT, Unit.KWH, self.energy_throughput))
        self.print_results()

    def plot(self) -> None:
        data: LithiumIonData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.title, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=LithiumIonState.TIME)
        yaxis: [[Axis]] = list()
        yaxis.append([Axis(data=data.soc, label=LithiumIonState.SOC, color=PlotlyPlotting.Color.BLUE,
                          linestyle=PlotlyPlotting.Linestyle.SOLID),
                      Axis(data=data.capacity * 1000, label=LithiumIonState.CAPACITY, color=PlotlyPlotting.Color.BLUE,
                          linestyle=PlotlyPlotting.Linestyle.SOLID)])
        yaxis.append([Axis(data=data.resistance, label=LithiumIonState.INTERNAL_RESISTANCE,
                           color=PlotlyPlotting.Color.BLUE, linestyle=PlotlyPlotting.Linestyle.SOLID),
                      Axis(data=data.temperature, label=LithiumIonState.TEMPERATURE, color=PlotlyPlotting.Color.BLUE,
                          linestyle=PlotlyPlotting.Linestyle.SOLID)])
        plot.subplots(xaxis=xaxis, yaxis=yaxis)
        self.extend_figures(plot.get_figures())

    @property
    def capacity_remaining(self) -> float:
        data: LithiumIonData = self.get_data()
        return data.state_of_health[-1] * 100