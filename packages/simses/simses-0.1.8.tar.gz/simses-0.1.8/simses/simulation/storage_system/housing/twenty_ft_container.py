from simses.simulation.storage_system.housing.housing import Housing
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model \
    import AmbientThermalModel
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.constant_ambient_temperature import \
    ConstantAmbientTemperature


class TwentyFtContainer(Housing):

    def __init__(self, ambient_thermal_model: AmbientThermalModel):
        super().__init__(ambient_thermal_model)

        # Container external dimensions (from mtcontainer)
        self.outer_length = 6.058  # m
        self.outer_breadth = 2.438  # m
        self.outer_height = 2.591  # m
        self.external_surface_area = self.outer_length * self.outer_height * 2 \
                                     + self.outer_height * self.outer_breadth * 2 \
                                     + self.outer_length * self.outer_breadth * 2  # in m2

        # Wall layer thicknesses
        self.thickness_L1 = 0.001  # m, L1 = layer 1 - Aluminium
        self.thickness_L2 = 0.015  # m, L2 = Layer 2 - polyurethane (up to 18mm)
        self.thickness_L3 = 0.0016  # m, L3 = Layer 3 - steel (1.6 mm)
        self.depth_corrugation = 0.03  # m (0.254)

        # Container internal dimensions
        self.inner_length = self.outer_length - 2 * (
                    self.thickness_L1 + self.thickness_L2 + self.thickness_L3 + self.depth_corrugation)  # in m
        self.inner_breadth = self.outer_breadth - 2 * (
                    self.thickness_L1 + self.thickness_L2 + self.thickness_L3 + self.depth_corrugation)  # m
        self.inner_height = self.outer_height - 2 * (
                    self.thickness_L1 + self.thickness_L2 + self.thickness_L3 + self.depth_corrugation)  # m
        self.__internal_surface_area = self.inner_length * self.inner_height * 2 \
                                       + self.inner_height * self.inner_breadth * 2 \
                                       + self.inner_length * self.inner_breadth * 2  # in m2
        self.__internal_volume = self.inner_length * self.inner_breadth * self.inner_height  # m3, 30 for 20 ft container (approx.).

        self.mean_surface_area = (self.external_surface_area + self.__internal_surface_area) / 2  # m2, midway: wall thickness

        # Mass of container inner and outer layers
        self.__density_L1_material = 2700  # kg/m3 (for Aluminium)
        self.__volume_L1_material = self.__internal_surface_area * self.thickness_L1
        self.mass_L1 = self.__volume_L1_material * self.__density_L1_material

        self.__density_L2_material = 35  # kg/m3 (for PU)
        self.__volume_L2_material = self.mean_surface_area * self.thickness_L2
        self.mass_L2 = self.__volume_L2_material * self.__density_L2_material

        self.__density_L3_material = 8050  # kg/m3 (for Steel)
        self.__volume_L3_material = self.external_surface_area * self.thickness_L3
        self.mass_L3 = self.__volume_L3_material * self.__density_L3_material

        # Container material thermal characteristics
        self.thermal_conductivity_L1 = 237  # W/mK  (for Aluminium)
        self.thermal_conductivity_L2 = 0.022  # W/mK (for PU)
        self.thermal_conductivity_L3 = 14.4  # W/mK (for Steel - Stainless, Type 304)
        self.specific_heat_L1 = 910   # J/kgK (for Aluminium)
        self.specific_heat_L2 = 1400  # J/kgK (for PU)
        self.specific_heat_L3 = 500  # J/kgK (for Steel - Stainless, Type 304)
        self.convection_coefficient_air_L1 = 30  # W/m2K, Convection coefficient for convection from air to L1 material (exemplary value)
        self.convection_coefficient_L3_air = 30  # W/m2K, Convection coefficient for convection from L3 material to air (exemplary value)

        # Initialize temperatures
        self.surface_temperature_L1 = self._initial_ambient_temperature  # K
        self.interface_temperature_L1_L2 = self._initial_ambient_temperature  # K
        self.temperature_L2 = self._initial_ambient_temperature
        self.interface_temperature_L2_L3 = self._initial_ambient_temperature  # K
        self.surface_temperature_L3 = self._initial_ambient_temperature  # K,
        # these are the temperatures of the surfaces facing the interior, in between, and exposed to the environment.
        # Initialized with ambient temperature

    @property
    def internal_volume(self) -> float:
        return self.__internal_volume * self._scale_factor

    @property
    def internal_surface_area(self) -> float:
        return self.__internal_surface_area * self._scale_factor


if __name__ == '__main__':  # Enables isolated debugging and execution of test cases
    print("This only executes when %s is executed rather than imported" % __file__)
    amb_model = ConstantAmbientTemperature()
    container = TwentyFtContainer(amb_model)
    vol = container.internal_air_volume
    print(vol)
