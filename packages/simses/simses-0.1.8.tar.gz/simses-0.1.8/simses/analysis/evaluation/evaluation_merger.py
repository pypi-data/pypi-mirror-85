import webbrowser

from simses.analysis.evaluation.evaluation import Evaluation
from simses.analysis.evaluation.plotting.plotting import Plotting
from simses.commons.state.system_parameters import SystemParameters
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig


class EvaluationMerger:

    """
    EvaluationMerger merges all evaluations results and figures into one HTML file and opens it after finishing.
    """

    OUTPUT_NAME: str = 'merged.html'

    def __init__(self, result_path: str, config: GeneralAnalysisConfig):
        self.__file_name: str = result_path + '/' + self.OUTPUT_NAME
        self.__system_parameters: str = result_path + '/' + SystemParameters().get_file_name()
        self.__merge_results: bool = config.merge_analysis

    def merge(self, evaluations: [Evaluation]) -> None:
        """
        Writes html file from evaluation results and figures.

        Parameters:
            evaluations:   List of evaluations.
        """
        if not self.__merge_results:
            return
        with open(self.__file_name, 'w') as outfile:
            outfile.write("<!DOCTYPE html><html><head></head><body>")
            self.__write_evaluations(evaluations, outfile)
            outfile.write("<br>")
            self.__write_system_parameters(outfile)
            outfile.write("</body></html>")
        webbrowser.open(self.__file_name, new=2)  # open in new tab

    def __write_evaluations(self, evaluations: [Evaluation], outfile) -> None:
        for evaluation in evaluations:
            if evaluation.should_be_considered:
                outfile.write("<section><b>" + evaluation.get_file_name() + "</b></section>")
                for result in evaluation.evaluation_results:
                    outfile.write(result.to_console() + "<br>")
                for figure in evaluation.get_figures():
                    outfile.write(Plotting.convert_to_html(figure))
                outfile.write("<br><br>")

    def __write_system_parameters(self, outfile) -> None:
        with open(self.__system_parameters, 'r') as system_parameters:
            lines: [str] = system_parameters.readlines()
            for line in lines:
                outfile.write(line)
