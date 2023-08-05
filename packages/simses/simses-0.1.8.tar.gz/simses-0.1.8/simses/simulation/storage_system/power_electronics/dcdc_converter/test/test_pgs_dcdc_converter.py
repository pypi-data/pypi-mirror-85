import pytest

from simses.config.data.power_electronics_config import PowerElectronicsConfig
from simses.simulation.storage_system.power_electronics.dcdc_converter.pgs_dcdc_converter import PgsDcDcConverter


@pytest.fixture()
def uut(intermediate_circuit_voltage):
    return PgsDcDcConverter(intermediate_circuit_voltage, PowerElectronicsConfig())


@pytest.mark.parametrize('intermediate_circuit_voltage, voltage, dc_power, result',
                         [
                             (300, 100, -10000, -10000),
                             (300, 300, 10000, 10000),
                             (300, 400, -10000, -10000),
                             (600, 500, 10000, 10000),
                             (600, 600, -10000, -10000),
                             (600, 700, 10000, 10000),
                             (700, 600, -10000, -10000),
                             (700, 700, 10000, 10000),
                             (700, 800, -10000, -10000),
                             (800, 700, 10000, 10000),
                             (800, 800, -10000, -10000),
                             (800, 900, 10000, 10000)
                         ]
                         )
def test_dc_power_calculation(result, uut, voltage, dc_power):
    uut.calculate_dc_current(dc_power, voltage)
    assert uut.dc_power_intermediate_circuit <= result


@pytest.mark.parametrize('intermediate_circuit_voltage, voltage, dc_power, result',
                         [
                             (300, 100, -10000, 0),
                             (300, 300, 10000, 0),
                             (300, 400, -10000, 0),
                             (600, 500, 10000, 0),
                             (600, 600, -10000, 0),
                             (600, 700, 10000, 0),
                             (700, 600, -10000, 0),
                             (700, 700, 10000, 0),
                             (700, 800, -10000, 0),
                             (800, 700, 10000, 0),
                             (800, 800, -10000, 0),
                             (800, 900, 10000, 0)
                         ]
                         )
def test_dc_power_loss_calculation(result, uut, voltage, dc_power):
    uut.calculate_dc_current(dc_power, voltage)
    assert uut.dc_power_loss >= result


@pytest.mark.parametrize('intermediate_circuit_voltage, voltage, dc_power, result',
                         [
                             (300, 100, -10000, -10000 / 100),
                             (300, 300, 10000, 10000 / 300),
                             (300, 400, -10000, -10000 / 400),
                             (600, 500, 10000, 10000 / 500),
                             (600, 600, -10000, -10000 / 600),
                             (600, 700, 10000, 10000 / 700),
                             (700, 600, -10000, -10000 / 600),
                             (700, 700, 10000, 10000 / 700),
                             (700, 800, -10000, -10000 / 800),
                             (800, 700, 10000, 10000 / 700),
                             (800, 800, -10000, -10000 / 800),
                             (800, 900, 10000, 10000 / 900)
                         ]
                         )
def test_dc_current_calculation(result, uut, voltage, dc_power):
    uut.calculate_dc_current(dc_power, voltage)
    assert uut.dc_current <= result


@pytest.mark.parametrize('intermediate_circuit_voltage, voltage, dc_power, result',
                         [
                             (300, 100, -10000, -10000),
                             (300, 300, 10000, 10000),
                             (300, 400, -10000, -10000),
                             (600, 500, 10000, 10000),
                             (600, 600, -10000, -10000),
                             (600, 700, 10000, 10000),
                             (700, 600, -10000, -10000),
                             (700, 700, 10000, 10000),
                             (700, 800, -10000, -10000),
                             (800, 700, 10000, 10000),
                             (800, 800, -10000, -10000),
                             (800, 900, 10000, 10000)
                         ]
                         )
def test_reverse_dc_power_calculation(result, uut, voltage, dc_power):
    uut.reverse_calculate_dc_current(dc_power, voltage)
    assert uut.dc_power_intermediate_circuit >= result


@pytest.mark.parametrize('intermediate_circuit_voltage, voltage, dc_power, result',
                         [
                             (300, 100, -10000, 0),
                             (300, 300, 10000, 0),
                             (300, 400, -10000, 0),
                             (600, 500, 10000, 0),
                             (600, 600, -10000, 0),
                             (600, 700, 10000, 0),
                             (700, 600, -10000, 0),
                             (700, 700, 10000, 0),
                             (700, 800, -10000, 0),
                             (800, 700, 10000, 0),
                             (800, 800, -10000, 0),
                             (800, 900, 10000, 0)
                         ]
                         )
def test_reverse_dc_power_loss_calculation(result, uut, voltage, dc_power):
    uut.reverse_calculate_dc_current(dc_power, voltage)
    assert uut.dc_power_loss >= result


@pytest.mark.parametrize('intermediate_circuit_voltage, voltage, dc_power, result',
                         [
                             (300, 100, -10000, -10000 / 300),
                             (300, 300, 10000, 10000 / 300),
                             (300, 400, -10000, -10000 / 300),
                             (600, 500, 10000, 10000 / 600),
                             (600, 600, -10000, -10000 / 600),
                             (600, 700, 10000, 10000 / 600),
                             (700, 600, -10000, -10000 / 700),
                             (700, 700, 10000, 10000 / 700),
                             (700, 800, -10000, -10000 / 700),
                             (800, 700, 10000, 10000 / 800),
                             (800, 800, -10000, -10000 / 800),
                             (800, 900, 10000, 10000 / 800)
                         ]
                         )
def test_reverse_dc_current_calculation(result, uut, voltage, dc_power):
    uut.reverse_calculate_dc_current(dc_power, voltage)
    assert uut.dc_current >= result
