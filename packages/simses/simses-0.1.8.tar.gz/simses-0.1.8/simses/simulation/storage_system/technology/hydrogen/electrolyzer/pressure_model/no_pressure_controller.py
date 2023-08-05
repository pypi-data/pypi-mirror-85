from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_controller import \
    PressureController


class NoPressureController(PressureController):

    def __init__(self):
        super().__init__()

    def calculate_n_h2_out(self, pressure_cathode, pressure_cathode_desire, n_h2_produced, max_n_h2_out) -> float:
        return n_h2_produced

    def calculate_n_o2_out(self, pressure_anode, pressure_anode_desire, n_o2_produced) -> float:
        return n_o2_produced