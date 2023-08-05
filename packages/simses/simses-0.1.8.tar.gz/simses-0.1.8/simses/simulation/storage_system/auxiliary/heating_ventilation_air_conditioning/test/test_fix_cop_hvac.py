import pytest
from simses.simulation.storage_system.auxiliary.heating_ventilation_air_conditioning.fix_cop_hvac import \
    FixCOPHeatingVentilationAirConditioning


class TestFixCOPHeatingVentilationAirConditioning:
    max_thermal_power: int = 10000  # in W
    set_point_temperature: float = 30  # in °C
    thermal_power_required = list(range(max_thermal_power - 500, max_thermal_power + 500, 50))

    def create_model(self):
        return FixCOPHeatingVentilationAirConditioning(self.max_thermal_power, self.set_point_temperature)

    @pytest.mark.parametrize("thermal_power_requested", thermal_power_required)
    def test_run_air_conditioning(self, thermal_power_requested):
        uut = self.create_model()
        uut.run_air_conditioning(thermal_power_requested)
        if thermal_power_requested <= self.max_thermal_power:
            assert uut.get_thermal_power() == thermal_power_requested
        else:
            assert uut.get_thermal_power() == self.max_thermal_power
        assert uut.get_electric_power() == uut.get_thermal_power() / uut.get_cop()
