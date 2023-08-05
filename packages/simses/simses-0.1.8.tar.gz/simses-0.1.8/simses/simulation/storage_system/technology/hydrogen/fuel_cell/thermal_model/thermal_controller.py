from abc import ABC, abstractmethod


class ThermalController(ABC):
    """ This controller controls the temperature of the EL-stack by setting new values for the mass flow and the
    temperature of the water running through the stack. It is asumed that the water temperature coming out of the
    stack equals the stack temperature"""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate_water_flow(self, stack_temperature, max_water_flow_cell, min_water_flow_cell) -> float:
        pass

    @abstractmethod
    def calculate_water_temperature_in(self, stack_temperatur) -> float:
        pass
