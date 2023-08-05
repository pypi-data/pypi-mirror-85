import multiprocessing
import os
from multiprocessing import Queue

from simses.commons.utils.utils import remove_all_files_from, create_directory_for
from simses.constants_simses import ROOT_PATH, BATCH_DIR
from simses.main import SimSES


class BatchSimulation(multiprocessing.Process):

    """
    BatchSimulation wraps the SimSES simulation into a multiprocessing Process in order to allow to run simulation
    in parallel. In addition, it is possible to run multiple threaded simulations within this process but this is
    strongly not recommended.
    """

    def __init__(self, config_set: dict, printer_queue: Queue, path: str = ROOT_PATH + 'results/', batch_size: int = 1,
                 do_simulation: bool = True, do_analysis: bool = True):
        super().__init__()
        batch_dir: str = os.path.join(path, BATCH_DIR)
        create_directory_for(batch_dir)
        remove_all_files_from(batch_dir)
        self.__path: str = os.path.join(path)
        self.__batch_size: int = batch_size
        self.__printer_queue: Queue = printer_queue
        self.__config_set: dict = config_set
        self.__do_simulation: bool = do_simulation
        self.__do_analysis: bool = do_analysis

    def __setup(self) -> [SimSES]:
        simulations: [SimSES] = list()
        for name, config in self.__config_set.items():
            remove_all_files_from(os.path.join(self.__path, name))
            simulations.append(SimSES(self.__path, name, do_simulation=self.__do_simulation, do_analysis=self.__do_analysis,
                                      simulation_config=config, queue=self.__printer_queue))
        return simulations

    def run(self):
        started: [SimSES] = list()
        simulations: [SimSES] = self.__setup()
        self.__check_simulation_names(simulations)
        for simulation in simulations:
            print('\rStarting ' + simulation.name)
            simulation.start()
            started.append(simulation)
            if len(started) >= self.__batch_size:
                self.__wait_for(started)
                started.clear()
        self.__wait_for(started)

    @staticmethod
    def __wait_for(simulations: [SimSES]):
        for simulation in simulations:
            simulation.join()

    @staticmethod
    def __check_simulation_names(simulations: [SimSES]) -> None:
        names: [str] = list()
        for simulation in simulations:
            name: str = simulation.name
            if name in names:
                raise Exception(name + ' is not unique. Please check your simulation setup!')
            names.append(name)
