from simses.commons.state.technology.storage_technology_state import StorageTechnologyState


class RedoxFlowState(StorageTechnologyState):
    """
    Current physical state of the redox flow system with the main electrical parameters.
    """

    SYSTEM_AC_ID = 'StorageSystemAC'
    SYSTEM_DC_ID = 'StorageSystemDC'
    SOC = 'SOC in p.u.'
    SOC_STACK = 'SOC in cell of the Stack in p.u.'
    SOH = 'State of health in p.u.'
    VOLTAGE = 'U in V'
    OPEN_CIRCUIT_VOLTAGE = 'OCV in V'
    CURRENT = 'I in A'
    CAPACITY = 'C in Wh'
    INTERNAL_RESISTANCE = 'Internal resistance in Ohm'
    POWER_LOSS = 'P_loss in W'
    POWER_IN = 'P_input in W'
    POWER = 'P_output in W'
    PUMP_POWER = 'P_pump in W'
    PRESSURE_LOSS_ANOLYTE = 'pressure loss anolyte in W'
    PRESSURE_LOSS_CATHOLYTE = 'pressure loss catholyte in W'
    FLOW_RATE_ANOLYTE = 'Anolyte flow rate in m^3/s'
    FLOW_RATE_CATHOLYTE = 'Catholyte flow rate in m^3/s'
    PRESSURE_DROP_ANOLYTE = 'Anolyte pressure drop in Pa'
    PRESSURE_DROP_CATHOLYTE = 'Catholyte pressure drop in Pa'
    FULFILLMENT = 'Fulfillment in p.u.'
    ELECTROLYTE_TEMPERATURE = 'Electrolyte temperature in K'
    TEMPERATURE = 'Cell temperature in K'
    TIME_PUMP = 'Time of Pump on or off in s'

    def __init__(self, system_id: int, storage_id: int):
        super().__init__()
        self._initialize()
        self.set(self.SYSTEM_AC_ID, system_id)
        self.set(self.SYSTEM_DC_ID, storage_id)

    @property
    def soc(self) -> float:
        return self.get(self.SOC)

    @soc.setter
    def soc(self, value: float) -> None:
        self.set(self.SOC, value)

    @property
    def soc_stack(self) -> float:
        return self.get(self.SOC_STACK)

    @soc_stack.setter
    def soc_stack(self, value: float) -> None:
        self.set(self.SOC_STACK, value)

    @property
    def voltage(self) -> float:
        return self.get(self.VOLTAGE)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.set(self.VOLTAGE, value)

    @property
    def open_circuit_voltage(self) -> float:
        """
        Open circuit voltage (OCV) in V

        Returns
        -------

        """
        return self.get(self.OPEN_CIRCUIT_VOLTAGE)

    @open_circuit_voltage.setter
    def open_circuit_voltage(self, value: float) -> None:
        self.set(self.OPEN_CIRCUIT_VOLTAGE, value)

    @property
    def soh(self) -> float:
        return self.get(self.SOH)

    @soh.setter
    def soh(self, value: float) -> None:
        self.set(self.SOH, value)

    @property
    def current(self) -> float:
        """
        Current in A

        Returns
        -------

        """
        return self.get(self.CURRENT)

    @current.setter
    def current(self, value: float) -> None:
        self.set(self.CURRENT, value)

    @property
    def capacity(self) -> float:
        return self.get(self.CAPACITY)

    @capacity.setter
    def capacity(self, value: float) -> None:
        self.set(self.CAPACITY, value)

    @property
    def internal_resistance(self) -> float:
        """
        Internal resistance in Ohm

        Returns
        -------

        """
        return self.get(self.INTERNAL_RESISTANCE)

    @internal_resistance.setter
    def internal_resistance(self, value: float) -> None:
        self.set(self.INTERNAL_RESISTANCE, value)

    @property
    def power_loss(self) -> float:
        return self.get(self.POWER_LOSS)

    @power_loss.setter
    def power_loss(self, value: float) -> None:
        self.set(self.POWER_LOSS, value)

    @property
    def power_in(self) -> float:
        """
        Input power in W

        Returns
        -------

        """
        return self.get(self.POWER_IN)

    @power_in.setter
    def power_in(self, value: float) -> None:
        self.set(self.POWER_IN, value)

    @property
    def power(self) -> float:
        """
        Output storage power in W

        Returns
        -------

        """
        return self.get(self.POWER)

    @power.setter
    def power(self, value: float) -> None:
        self.set(self.POWER, value)

    @property
    def pump_power(self) -> float:
        """
        Pump power in W

        Returns
        -------

        """
        return self.get(self.PUMP_POWER)

    @pump_power.setter
    def pump_power(self, value: float) -> None:
        self.set(self.PUMP_POWER, value)

    @property
    def pressure_loss_anolyte(self) -> float:
        """
        pressure loss anolyte in W

        Returns
        -------

        """
        return self.get(self.PRESSURE_LOSS_ANOLYTE)

    @pressure_loss_anolyte.setter
    def pressure_loss_anolyte(self, value: float) -> None:
        self.set(self.PRESSURE_LOSS_ANOLYTE, value)

    @property
    def pressure_loss_catholyte(self) -> float:
        """
        pressure loss catholyte in W

        Returns
        -------

        """
        return self.get(self.PRESSURE_LOSS_CATHOLYTE)

    @pressure_loss_catholyte.setter
    def pressure_loss_catholyte(self, value: float) -> None:
        self.set(self.PRESSURE_LOSS_CATHOLYTE, value)

    @property
    def flow_rate_anolyte(self) -> float:
        """
        Anolyte flow rate in m³/s

        Returns
        -------

        """
        return self.get(self.FLOW_RATE_ANOLYTE)

    @flow_rate_anolyte.setter
    def flow_rate_anolyte(self, value: float) -> None:
        self.set(self.FLOW_RATE_ANOLYTE, value)

    @property
    def flow_rate_catholyte(self) -> float:
        """
        Catholyte flow rate in m³/s

        Returns
        -------

        """
        return self.get(self.FLOW_RATE_CATHOLYTE)

    @flow_rate_catholyte.setter
    def flow_rate_catholyte(self, value: float) -> None:
        self.set(self.FLOW_RATE_CATHOLYTE, value)

    @property
    def pressure_drop_anolyte(self) -> float:
        """
        Anolyte pressure drop in Pa

        Returns
        -------

        """
        return self.get(self.PRESSURE_DROP_ANOLYTE)

    @pressure_drop_anolyte.setter
    def pressure_drop_anolyte(self, value: float) -> None:
        self.set(self.PRESSURE_DROP_ANOLYTE, value)

    @property
    def pressure_drop_catholyte(self) -> float:
        """
        Catholyte pressure drop in Pa

        Returns
        -------

        """
        return self.get(self.PRESSURE_DROP_CATHOLYTE)

    @pressure_drop_catholyte.setter
    def pressure_drop_catholyte(self, value: float) -> None:
        self.set(self.PRESSURE_DROP_CATHOLYTE, value)

    @property
    def fulfillment(self) -> float:
        return self.get(self.FULFILLMENT)

    @fulfillment.setter
    def fulfillment(self, value: float) -> None:
        self.set(self.FULFILLMENT, value)

    @property
    def electrolyte_temperature(self) -> float:
        """
        Temperature of the electrolyte in K

        Returns
        -------

        """
        return self.get(self.ELECTROLYTE_TEMPERATURE)

    @electrolyte_temperature.setter
    def electrolyte_temperature(self, value: float) -> None:
        self.set(self.ELECTROLYTE_TEMPERATURE, value)

    @property
    def temperature(self) -> float:
        return self.get(self.TEMPERATURE)

    @temperature.setter
    def temperature(self, value: float) -> None:
        self.set(self.TEMPERATURE, value)

    @property
    def time_pump(self) -> float:
        return self.get(self.TIME_PUMP)

    @time_pump.setter
    def time_pump(self, value: float) -> None:
        self.set(self.TIME_PUMP, value)

    @property
    def id(self) -> str:
        return 'REDOXFLOW' + str(self.get(self.SYSTEM_AC_ID)) + str(self.get(self.SYSTEM_DC_ID))

    @property
    def is_charge(self) -> bool:
        return self.power > 0

    @classmethod
    def sum_parallel(cls, states: []):
        pass

    @classmethod
    def sum_serial(cls, states: []):
        pass
