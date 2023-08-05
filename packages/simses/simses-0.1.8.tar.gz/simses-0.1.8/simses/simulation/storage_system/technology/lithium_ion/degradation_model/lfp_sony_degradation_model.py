from simses.config.simulation.battery_config import BatteryConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.\
    lfp_sony_calendar_degradation_model import SonyLFPCalendarDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.cycle_detector import \
    CycleDetector
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cyclic_degradation_model.\
    lfp_sony_cyclic_degradation_model import SonyLFPCyclicDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.degradation_model import DegradationModel


class SonyLFPDegradationModel(DegradationModel):

    def __init__(self, cell_type: CellType, cycle_detector: CycleDetector, battery_config: BatteryConfig):
        super().__init__(cell_type, SonyLFPCyclicDegradationModel(cell_type, cycle_detector),
                         SonyLFPCalendarDegradationModel(cell_type), cycle_detector, battery_config)
