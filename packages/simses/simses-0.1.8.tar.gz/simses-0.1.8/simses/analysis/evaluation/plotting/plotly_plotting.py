import plotly.graph_objects as go
from plotly.subplots import make_subplots

from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotting import Plotting


class PlotlyPlotting(Plotting):

    static_figure_index = 1

    class Color: #Using the TUM colors
        BLUE = '#0065BD'
        YELLOW = '#FFDC00'
        GREEN = '#A2AD00'
        RED = '#FF4136'
        CYAN = '#98C6EA'
        MAGENTA = '#F012BE'
        BLACK = '#000000'
        WHITE = '#FFFFFF'

    class Linestyle: #TODO Unused
        DOTTED = ':'
        SOLID = '-'
        DASHED = '--'
        DASH_DOT = '-.'

    def __init__(self, title: str, path: str):
        super().__init__()
        self.__title = title
        self.__path = path
        self.__figures: list = list()

    def layout(self, fig, xaxis: Axis, yaxis: [Axis]):
        if len(yaxis) == 1:
            yaxistitle = yaxis[0].label
        else:
            yaxistitle = ""
        fig.layout.title = self.__title
        fig.layout.font = dict(
                family="Times New Roman, monospace",  # TUM Guideline: Helvetica
                size=18,
                # color="#7f7f7f"
            )
        fig.update_layout(
            xaxis_title=xaxis.label,
            yaxis_title=yaxistitle,
            yaxis=dict(
                showexponent='all',
                exponentformat='e'
            ),
            showlegend=True,
            template="none",
        )
        fig.update_xaxes(showgrid=True, gridwidth=2, gridcolor='Lightgray',
                         showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showgrid=True, gridwidth=2, gridcolor='Lightgray',
                         showline=True, linewidth=2, linecolor='black')

    def lines(self, xaxis: Axis, yaxis: [Axis], secondary= []):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        self.layout(fig, xaxis, yaxis)
        fig.update_layout(legend=dict(x=0,y=1,traceorder="normal",))

        for i in range(len(yaxis)):
            if i in secondary:
                secondary_y_axis = True
            else:
                secondary_y_axis = False
            fig.add_trace(go.Scatter(
                x=xaxis.data,
                y=yaxis[i].data,
                mode='lines',
                name=yaxis[i].label,
                line_color=yaxis[i].color
                ), secondary_y=secondary_y_axis
            )
        self.show(fig)

    def get_figures(self) -> list:
        return self.__figures

    # @staticmethod
    # def convert_to_html(figure) -> str:
    #     return figure.to_html(auto_play= False,
    #                           include_plotlyjs=True,
    #                           include_mathjax=False,
    #                           #post_script=plot_id,
    #                           full_html=False,
    #                           #default_height=()),
    #                           validate=True
    #                           )

    def show(self, fig):
        self.__figures.append(fig)
        # pio.write_image(fig,
        #                 self.__path+self.alphanumerize(self.__title)+"_{}.svg".format(Plotting.static_figure_index),
        #                 format='svg',#or 'svg'
        #                 scale=None,#>1 increases resolution
        #                 width=1600,
        #                 height=800,
        #                 validate=True
        #                 )
        self.static_figure_index += 1

    def histogram(self):
        pass

    def subplots(self, xaxis: Axis, yaxis: [[Axis]]):
        fig = make_subplots(rows=len(yaxis), cols=len(yaxis[0]))
        for x in range(len(yaxis)):
            ydata = yaxis[x]
            for y in range(len(ydata)):

                fig.append_trace(go.Scatter(
                    x=xaxis.data,
                    y=ydata[y].data,
                    name=ydata[y].label,
                    line_color=ydata[y].color,
                ),
                row=y+1, col=x+1)
        self.layout(fig, xaxis, yaxis)
        self.show(fig)
