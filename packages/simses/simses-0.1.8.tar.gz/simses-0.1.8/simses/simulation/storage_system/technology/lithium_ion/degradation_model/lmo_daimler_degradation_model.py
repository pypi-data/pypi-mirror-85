from simses.config.simulation.battery_config import BatteryConfig
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.degradation_model import DegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.lfp_sony_calendar_degradation_model import \
    SonyLFPCalendarDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.nca_panasonicNCR_calendar_degradation_model import \
    PanasonicNCACalendarDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.nmc_molicel_calendar_degradation_model import \
    MolicelNMCCalendarDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.nmc_sanyo_ur18650e_calendar_degradation_model import \
    SanyoNMCCalendarDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.cycle_detector import \
    CycleDetector
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cyclic_degradation_model.lfp_sony_cyclic_degradation_model import \
    SonyLFPCyclicDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cyclic_degradation_model.nca_panasonicNCR_cyclic_degradation_model import \
    PanasonicNCACyclicDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cyclic_degradation_model.nmc_molicel_cyclic_degradation_model import \
    MolicelNMCCyclicDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cyclic_degradation_model.nmc_sanyo_ur18650e_cyclic_degradation_model import \
    SanyoNMCCyclicDegradationModel


class DaimlerLMODegradationModel(DegradationModel):
    """ Degradation Model for Second-Life cell. Specific model unknown, therefore using different existing
    degradation models from SimSES."""

    def __init__(self, cell_type: CellType, cycle_detector: CycleDetector, battery_config: BatteryConfig):
        super().__init__(cell_type, MolicelNMCCyclicDegradationModel(cell_type, cycle_detector),
                         MolicelNMCCalendarDegradationModel(cell_type), cycle_detector, battery_config)
