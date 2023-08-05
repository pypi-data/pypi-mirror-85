import matplotlib.pyplot as plt

from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotting import Plotting


class MatplotPlotting(Plotting):

    class Color:
        BLUE = 'b'
        YELLOW = 'y'
        GREEN = 'g'
        RED = 'r'
        CYAN = 'c'
        MAGENTA = 'm'
        BLACK = 'k'
        WHITE = 'w'

    class Linestyle:
        DOTTED = ':'
        SOLID = '-'
        DASHED = '--'
        DASH_DOT = '-.'

    def __init__(self, title: str, path: str):
        super().__init__()
        self.__title = title
        self.__path = path

    def lines(self, xaxis: Axis, yaxis: [Axis], secondary=[]):
        plt.title(self.__title)
        # plt.ylabel(self.__ylabel)
        plt.xlabel(xaxis.label)
        for y in yaxis:
            plt.plot(xaxis.data, y.data, color=y.color, linestyle=y.linestyle, label=y.label)
        plt.legend()
        plt.grid()
        self.show()

    def show(self):
        plt.savefig(self.__path + self.alphanumerize(self.__title)+'.pdf')
        plt.show()

    def histogram(self):
        pass

    def subplots(self, xaxis: Axis, yaxis: [[Axis]]):
        fig, axes = plt.subplots(len(yaxis), len(yaxis[0]), figsize=(16, 9), squeeze=False)
        fig.suptitle(self.__title)
        for x in range(len(yaxis)):
            ydata = yaxis[x]
            for y in range(len(ydata)):
                axes[x, y].plot(xaxis.data, ydata[y].data)
                axes[x, y].set(xlabel=xaxis.label, ylabel='', title=ydata[y].label)
                axes[x, y].grid()
        self.show()

    # @staticmethod
    # def convert_to_html(figure) -> str:
    #     pass
