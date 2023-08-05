from simses.simulation.storage_system.dc_coupling.dc_coupling import DcCoupling
from simses.simulation.storage_system.dc_coupling.generation.no_dc_generation import NoDcGeneration
from simses.simulation.storage_system.dc_coupling.load.no_dc_load import NoDcLoad


class NoDcCoupling(DcCoupling):

    def __init__(self):
        super().__init__(NoDcLoad(), NoDcGeneration())
