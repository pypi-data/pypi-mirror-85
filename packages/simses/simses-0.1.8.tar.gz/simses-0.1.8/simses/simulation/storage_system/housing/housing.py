from abc import ABC, abstractmethod

from simses.commons.log import Logger


class Housing(ABC):
    """ class to specify the housing of the storage system"""

    def __init__(self, ambient_thermal_model):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self._initial_ambient_temperature: float = ambient_thermal_model.get_initial_temperature()  # (self.start_time)
        self._internal_component_volume: float = 0.0
        self._scale_factor: int = 1
        self._volume_usability_factor: float = 0.2

    def add_component_volume(self, volume: float):
        self._internal_component_volume += volume
        while self._internal_component_volume > self._volume_usability_factor * self.internal_volume:
            self._scale_factor += 1
            self.__log.info('Increasing number of containers to ' + str(self._scale_factor))

    @property
    @abstractmethod
    def internal_volume(self) -> float:
        """
        Returns internal volume of housing in m3

        Returns
        -------

        """
        pass

    @property
    def internal_air_volume(self) -> float:
        """
        Returns internal air volume of housing in m3

        Returns
        -------

        """
        return self.internal_volume - self._internal_component_volume

    @property
    @abstractmethod
    def internal_surface_area(self) -> float:
        pass

    def close(self) -> None:
        self.__log.close()

    def get_number_of_containers(self) -> int:
        return self._scale_factor
