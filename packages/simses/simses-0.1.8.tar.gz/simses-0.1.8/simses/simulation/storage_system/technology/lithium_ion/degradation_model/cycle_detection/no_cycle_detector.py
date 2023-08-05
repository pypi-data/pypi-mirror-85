from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.cycle_detector import \
    CycleDetector


class NoCycleDetector(CycleDetector):

    def __init__(self):
        super().__init__()

    def cycle_detected(self, time: float, battery_state: LithiumIonState) -> bool:
        return False

    def get_depth_of_cycle(self) -> float:
        return 0

    def get_delta_full_equivalent_cycle(self) -> float:
        return 0

    def get_crate(self) -> float:
        return 0

    def get_full_equivalent_cycle(self) -> float:
        return 0

    def _update_cycle_steps(self, soc: float, time_passed: float) -> None:
        pass

    def _reset_cycle(self, soc:float, time_passed: float) -> None:
        pass

    def reset(self) -> None:
        pass

    def close(self) -> None:
        pass
