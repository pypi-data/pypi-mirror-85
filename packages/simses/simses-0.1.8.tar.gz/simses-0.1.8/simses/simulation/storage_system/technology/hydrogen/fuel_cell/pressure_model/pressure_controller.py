from abc import ABC, abstractmethod


class PressureController(ABC):
    """ This controller controls the pressure of anode and cathode side of the electrolyzer like a control valve"""
    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate_n_h2_in(self, pressure_anode, pressure_anode_desire, n_h2_used) -> float:
        pass

    @abstractmethod
    def calculate_n_o2_in(self, pressure_cathode, pressure_cathode_desire, n_o2_used) -> float:
        pass