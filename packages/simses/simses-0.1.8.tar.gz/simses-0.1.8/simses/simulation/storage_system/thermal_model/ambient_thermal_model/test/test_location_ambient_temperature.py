import pytest
from simses.config.data.temperature_data_config import TemperatureDataConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.location_ambient_temperature import \
    LocationAmbientTemperature


class TestLocationAmbientTemperature:
    config = None
    general_config: GeneralSimulationConfig = GeneralSimulationConfig(config)
    temperature_config: TemperatureDataConfig = TemperatureDataConfig()
    start_time = int(general_config.start)
    duration = int(general_config.duration)
    sample_time = int(general_config.timestep)
    time_step_range = list(range(start_time, start_time + duration, 4 * sample_time))

    def create_model(self) -> LocationAmbientTemperature:
        return LocationAmbientTemperature(self.temperature_config, self.general_config)

    @pytest.mark.parametrize("time_step", time_step_range)
    def test_get_temperature(self, time_step):
        uut = self.create_model()
        assert uut.get_temperature(time_step) > 190.35  # K,
        assert uut.get_initial_temperature() > 190.35  # K,
        # not colder than the coldest temperature recorded on earth
        assert uut.get_temperature(time_step) < 329.85  # K,
        assert uut.get_initial_temperature() < 329.85  # K,
        # not hotter than the hottest temperature recorded on earth
