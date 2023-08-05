from simses.config.simulation.battery_config import BatteryConfig
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.degradation_model import DegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.\
    no_calendar_dedradation import NoCalendarDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.cycle_detector import \
    CycleDetector
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cyclic_degradation_model.\
    no_cyclic_degradation import NoCyclicDegradationModel


class NoDegradationModel(DegradationModel):

    def __init__(self, cell: CellType, cycle_detector:CycleDetector, battery_config: BatteryConfig):
        super().__init__(cell, NoCyclicDegradationModel(), NoCalendarDegradationModel(), cycle_detector, battery_config)