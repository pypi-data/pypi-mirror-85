from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter import AcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.m2b_acdc_converter import M2bAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.notton_acdc_converter import NottonAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.sinamics_acdc_converter import \
    Sinamics120AcDcConverter


class AcDcConverterMultipleStacked:

    def __init__(self, number_converters: int, switch_value: float,
                 acdc_converter: AcDcConverter):
        self._MAX_POWER: float = acdc_converter.max_power * number_converters
        self._NUMBER_CONVERTERS = number_converters
        self._SWITCH_VALUE = switch_value  # ratio power over rated power
        #  Work-in-progress
        # TODO Use AcDcConverterIdenticalStacked as guide template


    def to_ac(self, power: float, voltage: float) -> float:
        switch_value = self._SWITCH_VALUE
        if power == 0:
            return 0
        else:
            power_individual = self.power_splitter(power)

        power_individual_dc = [0] * len(power_individual)
        for i in range(0, len(power_individual), 1):
            power_individual_dc[i] = self.__converters[i].to_ac(power_individual[i], voltage)

        return sum(power_individual_dc)

    def to_dc(self, power: float, voltage: float) -> float:
        if power == 0:
            return 0
        else:
            power_individual = self.power_splitter(power)

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

        """
        pass

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

        """
        pass

    def power_splitter(self, power: float) -> float:
        #  Work-in-progress
        # TODO Use siemens_acdc_converter_stacked power splitter logic as guide template
        a = 0  # dummy
        return a  # dummy

    def max_power(self) -> float:
        return self._MAX_POWER

    def number_converters(self) -> int:
        return self._NUMBER_CONVERTERS

    def switch_value(self) -> float:
        return self._SWITCH_VALUE

    def close(self) -> None:
        """Closing all resources in acdc converter"""
        pass


if __name__ == '__main__':  # Enables isolated debugging and execution of test cases
    print("This only executes when %s is executed rather than imported" % __file__)

    notton_power = 3000
    notton_number = 2
    siemens_power = 1000
    siemens_number = 2
    m2b_power = 1500
    m2b_number = 1

    total_power = notton_power*notton_number + siemens_power*siemens_number + m2b_power*m2b_number

    notton_converters = [NottonAcDcConverter(notton_power)] * notton_number
    siemens_converters = [Sinamics120AcDcConverter(siemens_power)] * siemens_number
    m2b_converters = [M2bAcDcConverter(m2b_power)] * m2b_number

    acdc_converter = notton_converters + siemens_converters + m2b_converters
    stacked_conv = AcDcConverterMultipleStacked(5, 0.9, acdc_converter)
    dc_power_1 = stacked_conv.to_ac(10000, 400)  # Voltage is a dummy variable here
    print(dc_power_1)
    dc_power_2 = stacked_conv.to_dc(2000, 400)  # Voltage is a dummy variable here
    print(dc_power_2)