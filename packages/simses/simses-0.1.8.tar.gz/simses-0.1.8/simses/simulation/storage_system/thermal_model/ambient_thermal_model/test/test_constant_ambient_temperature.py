import pytest
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.constant_ambient_temperature import \
    ConstantAmbientTemperature


class TestConstantAmbientTemperature:
    constant_ambient_temperature_user_value = 25  # in C
    constant_ambient_temperature_internal_value = constant_ambient_temperature_user_value + 273.15  # in K

    time_step_range = list(range(0, 5, 1))

    def create_model(self):
        return ConstantAmbientTemperature(self.constant_ambient_temperature_user_value)

    @pytest.mark.parametrize("time_step", time_step_range)
    def test_get_temperature(self, time_step):
        uut = self.create_model()
        assert uut.get_temperature(time_step) == self.constant_ambient_temperature_internal_value
        assert uut.get_initial_temperature() == self.constant_ambient_temperature_internal_value
