from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model.pressure_controller import \
    PressureController


class VarCathodePressureController(PressureController):
    """ This pressure controller controls the cathode pressure at a disired level and keeps the anode pressure
    at ambient level"""
    def __init__(self):
        super().__init__()

    def calculate_n_h2_out(self, pressure_cathode, pressure_cathode_desire, n_h2_prod) -> float:
        if pressure_cathode < 0.9 * pressure_cathode_desire:
            return 0
        if pressure_cathode > 1.1 * pressure_cathode_desire:
            return 2 * n_h2_prod
        else:
            return n_h2_prod

    def calculate_n_o2_out(self, pressure_anode, pressure_anode_desire, n_o2_prod) -> float:
        return n_o2_prod