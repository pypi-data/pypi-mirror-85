from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_controller import \
    PressureController


class VarCathodePressureController(PressureController):
    """ This pressure controller controls the cathode pressure at a disired level and keeps the anode pressure
    at ambient level"""
    def __init__(self):
        super().__init__()

    def calculate_n_h2_out(self, pressure_cathode, pressure_cathode_desire, n_h2_prod, max_n_h2_out) -> float:
        if pressure_cathode < 0.99 * pressure_cathode_desire:
            return 0
        if pressure_cathode > 1.01 * pressure_cathode_desire:
            return max_n_h2_out
        else:
            if n_h2_prod >= 0:
                return n_h2_prod
            else:
                return 0  # no intake of atmosphere in case of negative hydrogen production (-> only permeation)

    def calculate_n_o2_out(self, pressure_anode, pressure_anode_desire, n_o2_prod) -> float:
        if n_o2_prod >= 0:
            return n_o2_prod
        else:
            return 0  # no intake of atmosphere in case of negative oxygen production (-> only permeation)