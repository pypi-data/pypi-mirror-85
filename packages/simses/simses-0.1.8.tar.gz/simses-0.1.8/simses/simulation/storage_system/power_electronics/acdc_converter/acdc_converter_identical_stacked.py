from numpy.core._multiarray_umath import sign

from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter import AcDcConverter


class AcDcConverterIdenticalStacked(AcDcConverter):

    def __init__(self, number_converters: int, switch_value: float, acdc_converter: AcDcConverter, power_electronics_config=None):
        super().__init__(acdc_converter.max_power)
        self._NUMBER_CONVERTERS = number_converters
        self._SWITCH_VALUE = switch_value  # ratio power over rated power
        self._MAX_POWER_INDIVIDUAL = acdc_converter.max_power / number_converters
        self.__converters: [AcDcConverter] = list()
        for converter in range(number_converters):
            self.__converters.append(acdc_converter.create_instance(self._MAX_POWER_INDIVIDUAL, power_electronics_config))

    def to_ac(self, power: float, voltage: float) -> float:
        if power == 0:
            return 0
        else:
            power_individual = self.__power_splitter(power)

        power_individual_dc = [0] * len(power_individual)
        for i in range(0, len(power_individual), 1):
            power_individual_dc[i] = self.__converters[i].to_ac(power_individual[i], voltage)

        return sum(power_individual_dc)

    def to_dc(self, power: float, voltage: float) -> float:
        if power == 0:
            return 0
        else:
            power_individual = self.__power_splitter(power)

        power_individual_dc = [0] * len(power_individual)
        for i in range(0, len(power_individual), 1):
            power_individual_dc[i] = self.__converters[i].to_dc(power_individual[i], voltage)

        return sum(power_individual_dc)

    def to_dc_reverse(self, dc_power: float) -> float:
        """
        recalculates ac power in W, if the BMS limits the DC_power

        Parameters
        ----------
        voltage_input : float
        current : float

        Returns
        -------
        float
            dc power in W
            :param dc_power:

        """
        if dc_power == 0:
            return 0.0
        else:
            power_individual = self.__power_splitter(dc_power)

        power_individual_dc = [0] * len(power_individual)
        for i in range(0, len(power_individual), 1):
            power_individual_dc[i] = self.__converters[i].to_dc_reverse(power_individual[i])

        return sum(power_individual_dc)

    def to_ac_reverse(self, dc_power: float) -> float:
        """
        recalculates ac power in W, if the BMS limits the DC_power

        Parameters
        ----------
        voltage_input : float
        current : float

        Returns
        -------
        float
            dc power in W
            :param dc_power:

        """
        if dc_power == 0:
            return 0.0
        else:
            power_individual = self.__power_splitter(dc_power)

        power_individual_dc = [0] * len(power_individual)
        for i in range(0, len(power_individual), 1):
            power_individual_dc[i] = self.__converters[i].to_ac_reverse(power_individual[i])

        return sum(power_individual_dc)

    def __power_splitter(self, power: float) -> list:
        power_individual = [0] * self._NUMBER_CONVERTERS
        switch_value = self._SWITCH_VALUE

        if switch_value >= 0.8 and abs(power) >= switch_value * self._MAX_POWER and abs(power) < self._MAX_POWER:
            switch_value = 1
        elif switch_value >= 0.8 and switch_value * self._MAX_POWER_INDIVIDUAL <= abs(power) <= self._MAX_POWER_INDIVIDUAL:
            switch_value = 1

        if abs(power) >= self._MAX_POWER:
            # TODO check which error occurs here and why
            try:
                power_individual[:] = self._MAX_POWER_INDIVIDUAL * sign(power)
            except:
                pass
        elif abs(power) <= self._MAX_POWER_INDIVIDUAL * switch_value:
            power_individual[0] = power
        else:
            number_converters_switch_value = int(abs(int(power // (self._MAX_POWER_INDIVIDUAL * switch_value))))
            power_individual[0:number_converters_switch_value] = [self._MAX_POWER_INDIVIDUAL * switch_value] * number_converters_switch_value
            if number_converters_switch_value < self._NUMBER_CONVERTERS:
                power_individual[number_converters_switch_value] = power - number_converters_switch_value * self._MAX_POWER_INDIVIDUAL * switch_value
            if abs(power) <= number_converters_switch_value * self._MAX_POWER_INDIVIDUAL:
                power_individual[0:number_converters_switch_value] = [power / number_converters_switch_value] * number_converters_switch_value
                try:
                    power_individual[number_converters_switch_value] = 0
                except IndexError:
                    pass

        return power_individual

    @property
    def volume(self) -> float:
        volume: float = 0.0
        for converter in self.__converters:
            volume += converter.volume
        return volume

    @property
    def mass(self):
        mass: float = 0.0
        for converter in self.__converters:
            mass += converter.mass
        return mass

    @property
    def surface_area(self) -> float:
        surface_area: float = 0.0
        for converter in self.__converters:
            surface_area += converter.surface_area
        return surface_area

    def close(self) -> None:
        """Closing all resources in acdc converter"""
        for converter in self.__converters:
            converter.close()

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config=None):
        pass

