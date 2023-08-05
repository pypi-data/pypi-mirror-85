from abc import ABC, abstractmethod


class Parameters(ABC):

    """Class to import parameters out of a csv-file into a model"""

    def __init__(self):
        pass

    # def update(self) -> None:
    #     self.import_parameters()
    #
    # # @abstractmethod
    # # def import_parameters(self) -> None:
    # #     pass