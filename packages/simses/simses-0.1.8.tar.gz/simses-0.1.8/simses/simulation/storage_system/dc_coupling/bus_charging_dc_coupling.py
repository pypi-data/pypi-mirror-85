from simses.simulation.storage_system.dc_coupling.dc_coupling import DcCoupling
from simses.simulation.storage_system.dc_coupling.generation.pv_dc_generation import PvDcGeneration
from simses.simulation.storage_system.dc_coupling.load.dc_bus_charging_fixed import DcBusChargingFixed


class BusChargingDcCoupling(DcCoupling):

    def __init__(self, charging_power: float, generation_power: float):
        super().__init__(DcBusChargingFixed(charging_power), PvDcGeneration(generation_power))
