import csv
import os

import numpy

from simses.commons.utils.utils import format_float
from simses.config.data.power_electronics_config import PowerElectronicsConfig
from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter import AcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter_identical_stacked import \
    AcDcConverterIdenticalStacked
from simses.simulation.storage_system.power_electronics.acdc_converter.notton_acdc_converter import NottonAcDcConverter
from simses.simulation.storage_system.power_electronics.acdc_converter.sinamics_acdc_converter import \
    Sinamics120AcDcConverter


def create_line_from(name: str, values: [float]) -> [str]:
    line: [str] = list()
    line.append(name)
    for value in values:
        line.append(format_float(value, decimals=4))
    return line


if __name__ == "__main__":
    max_power: float = 1e6
    config: PowerElectronicsConfig = PowerElectronicsConfig()
    voltage: float = 700
    power_range: [int] = range(-int(max_power), int(max_power), int(max_power / 200))
    file_name: str = os.path.dirname(__file__) + '/comparison.csv'

    converters: [AcDcConverter] = list()
    converters.append(NottonAcDcConverter(max_power))
    converters.append(Sinamics120AcDcConverter(max_power, config))
    converters.append(AcDcConverterIdenticalStacked(10, 1, NottonAcDcConverter(max_power), config))

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(create_line_from('Power', numpy.array(power_range) / max_power))
        for converter in converters:
            efficiencies: [float] = list()
            for power in power_range:
                if power > 0:
                    power_dc: float = converter.to_dc(power, voltage)
                    try:
                        eff: float = power_dc / power
                    except ZeroDivisionError:
                        eff: float = 0.0
                    efficiencies.append(eff)
                else:
                    power_dc: float = converter.to_ac(power, voltage)
                    try:
                        eff: float = power / power_dc
                    except ZeroDivisionError:
                        eff: float = 0.0
                    efficiencies.append(eff)
            writer.writerow(create_line_from(type(converter).__name__, efficiencies))
