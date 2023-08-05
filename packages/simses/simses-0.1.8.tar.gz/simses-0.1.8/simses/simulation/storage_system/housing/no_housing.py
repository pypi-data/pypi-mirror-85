import numpy

from simses.simulation.storage_system.housing.housing import Housing
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model \
    import AmbientThermalModel


class NoHousing(Housing):

    LARGE_NUMBER = numpy.finfo(numpy.float64).max * 1e-100

    def __init__(self, ambient_thermal_model: AmbientThermalModel):
        super().__init__(ambient_thermal_model)

    @property
    def internal_volume(self) -> float:
        return self.LARGE_NUMBER

    @property
    def internal_surface_area(self) -> float:
        return self.LARGE_NUMBER
