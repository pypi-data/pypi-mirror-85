from simses.config.simulation.battery_config import BatteryConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.degradation_model import DegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.generic_cell_calendar_degradation_model import \
    GenericCellCalendarDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.cycle_detector import \
    CycleDetector
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cyclic_degradation_model.generic_cell_cyclic_degradation_model import \
    GenericCellCyclicDegradationModel


class GenericCellDegradationModel(DegradationModel):

    def __init__(self, cell_type: CellType, cycle_detector: CycleDetector, battery_config: BatteryConfig):
        super().__init__(cell_type, GenericCellCyclicDegradationModel(cell_type, cycle_detector, battery_config),
                         GenericCellCalendarDegradationModel(cell_type, battery_config), cycle_detector,
                         battery_config)