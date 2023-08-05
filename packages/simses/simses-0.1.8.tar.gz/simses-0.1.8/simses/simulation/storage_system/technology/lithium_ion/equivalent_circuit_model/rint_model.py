from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.commons.log import Logger
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.equivalent_circuit_model.equivalent_circuit_model import \
    EquivalentCircuitModel


class RintModel(EquivalentCircuitModel):

    def __init__(self, cell_type: CellType):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__cell_type: CellType = cell_type

    def update(self, time: float, battery_state: LithiumIonState) -> None:
        cell: CellType = self.__cell_type
        bs: LithiumIonState = battery_state
        dsoc = self.calculate_dsoc(time, bs, cell)
        bs.soc += dsoc
        self.__log.debug('Delta SOC: ' + str(dsoc))
        if bs.soc < 1e-7:
            self.__log.warn('SOC was tried to be set to a value of ' + str(bs.soc) + ' but adjusted to 0.')
            bs.soc = 0.0
        ocv: float = cell.get_open_circuit_voltage(bs)  # V
        rint = bs.internal_resistance
        bs.voltage = ocv + rint * bs.current
        bs.power_loss = rint * bs.current ** 2

    @staticmethod
    def calculate_dsoc(time: float, bs: LithiumIonState, cell: CellType) -> float:
        coulomb_eff = cell.get_coulomb_efficiency(bs)
        self_discharge_rate: float = cell.get_self_discharge_rate() * (time - bs.time)
        # Ah (better As) counting
        return (bs.current * (time - bs.time) / 3600.0) / (bs.capacity / bs.nominal_voltage) * coulomb_eff - self_discharge_rate

    def close(self) -> None:
        self.__log.close()
