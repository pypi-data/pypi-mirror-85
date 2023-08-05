import datetime
from abc import abstractmethod, ABC

import plotly

from simses.analysis.evaluation.plotting.axis import Axis


class Plotting(ABC):

    """
    Plotting is an abstract class providing the interfaces for different plotting engines.
    """

    def __init__(self):
        self.__figures: list = list()

    @abstractmethod
    def lines(self, xaxis: Axis, yaxis: [Axis], secondary: list = []):
        """
        Creates a figure object by adding traces from the passed axes.

        Parameters:
            xaxis: x-axis.
            yaxis: List of y-axes.
            secondary: List of secondary axes.
        """
        pass

    def get_figures(self) -> list:
        """
        Returns the list of figures saved in the instance of the plotting class instance.
        """
        return self.__figures

    @abstractmethod
    def histogram(self):
        pass

    @abstractmethod
    def subplots(self, xaxis: Axis, yaxis: [[Axis]]):
        """
        Creates a figure object consisting of subplots from passed axes.

        Parameters:
            xaxis: x-Axis.
            yaxis: Traces-list in subplot-list of y-axes.
        """
        pass

    def alphanumerize(self, string) -> str:
        """
        Returns a valid alphanumeric string that can be used for a filename.

        Parameters:
            string: String to be processed.
        """
        return ''.join(e for e in string if e.isalnum())

    @staticmethod
    def convert_to_html(figure) -> str:
        """
        Returns a string that can be embedded in an html from a passed figure object.

        Parameters:
            figure: Figure to be converted to a html-readable string.
        """
        if isinstance(figure, plotly.graph_objs.Figure):
            return figure.to_html(auto_play=False,
                                  include_plotlyjs=True,
                                  include_mathjax=False,
                                  # post_script=plot_id,
                                  full_html=False,
                                  # default_height=()),
                                  validate=True
                                  )

    @staticmethod
    def format_time(time_data):
        """
        Converts list of timestamps into a list of datetimes.

        Parameters:
            time_data: List of timestamps.
        """
        time = list()
        for tstmp in time_data:
            time.append(datetime.datetime.fromtimestamp(tstmp, tz=datetime.timezone.utc))
        return time
