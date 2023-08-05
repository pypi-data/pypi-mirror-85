from abc import ABC, abstractmethod

from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.auxiliary.pump.pump import Pump


class PumpAlgorithm(ABC):

    def __init__(self, pump: Pump):
        self.__pump: Pump = pump

    def update(self, redox_flow_state: RedoxFlowState) -> None:
        """
        Updates flow rate and pressure drop of the current redox_flow_state and starts the calculation of
        the pump_power.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            Current state of redox_flow.

        Returns
        -------

        """
        flow_rate_min = self.get_flow_rate_min()
        flow_rate_max = self.get_flow_rate_max()
        redox_flow_state.pressure_drop_catholyte = self.get_pressure_drop_catholyte(redox_flow_state)
        redox_flow_state.pressure_drop_anolyte = self.get_pressure_drop_anolyte(redox_flow_state)
        redox_flow_state.flow_rate_catholyte = self.get_flow_rate_catholyte(redox_flow_state)
        redox_flow_state.flow_rate_anolyte = self.get_flow_rate_anolyte(redox_flow_state)
        redox_flow_state.pressure_loss_catholyte = (redox_flow_state.flow_rate_catholyte *
                                                    redox_flow_state.pressure_drop_catholyte)
        redox_flow_state.pressure_loss_anolyte = (redox_flow_state.flow_rate_anolyte *
                                                  redox_flow_state.pressure_drop_anolyte)

        self.__pump.set_eta_pump(redox_flow_state.flow_rate_catholyte, flow_rate_max, flow_rate_min)
        self.__pump.calculate_pump_power(redox_flow_state.pressure_loss_catholyte)
        pump_power_catholyte = self.__pump.get_pump_power()

        self.__pump.set_eta_pump(redox_flow_state.flow_rate_anolyte, flow_rate_max, flow_rate_min)
        self.__pump.calculate_pump_power(redox_flow_state.pressure_loss_anolyte)
        pump_power_anolyte = self.__pump.get_pump_power()

        redox_flow_state.pump_power = pump_power_catholyte + pump_power_anolyte

    @abstractmethod
    def get_pressure_drop_anolyte(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Determines the pressure drop over the stack module and pipe system for the anolyte side in Pa.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            Current state of redox_flow.

        Returns
        -------
        float :
            Pressure drop of the anolyte side in Pa.
        """
        pass

    @abstractmethod
    def get_pressure_drop_catholyte(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Determines the pressure drop over the stack module and pipe system for the catholyte side in Pa.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            Current state of redox_flow.

        Returns
        -------
        float :
            Pressure drop of the catholyte side in Pa.
        """
        pass

    @abstractmethod
    def get_flow_rate_anolyte(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Determines the the flow rate of the anolyte side in m^3/s.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            Current state of redox_flow.

        Returns
        -------
        float :
            Flow rate of the anolyte side in m^3/s.
        """
        pass

    @abstractmethod
    def get_flow_rate_catholyte(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Determines the the flow rate of the catholyte side in m^3/s.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            Current state of redox_flow.

        Returns
        -------
        float :
            Flow rate of the catholyte side in m^3/s.
        """
        pass

    @abstractmethod
    def get_flow_rate_max(self) -> float:
        """
        Maximal needed flow rate in the system in m^3/s.

        Returns
        -------
        float:
            Maximal flow rate in m^3/s.
        """
        pass

    @abstractmethod
    def get_flow_rate_min(self) -> float:
        """
        Minimal needed flow rate in the system in m^3/s.

        Returns
        -------
        float:
            Minimal flow rate in m^3/s.
        """
        pass

    @abstractmethod
    def close(self):
        """Closing all resources in PumpAlgorithm."""
        self.__pump.close()
