from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.degradation_model.capacity_degradation_model import \
    CapacityDegradationModel


class NoDegradation(CapacityDegradationModel):
    """Model with no capacity degradation for a redox flow battery."""

    def __init__(self):
        super().__init__()

    def get_capacity_degradation(self, time: float, redox_flow_state: RedoxFlowState):
        return 0.0

    def close(self):
        super().close()
