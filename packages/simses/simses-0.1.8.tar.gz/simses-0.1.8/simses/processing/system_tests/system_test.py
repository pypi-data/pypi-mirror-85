import os
import shutil
import time
from configparser import ConfigParser

from simses.commons.utils.utils import remove_file
from simses.constants_simses import ROOT_PATH, CONFIG_PATH
from simses.processing.batch_processing import BatchProcessing


class TestBatchProcessing(BatchProcessing):

    """
    TestBatchProcessing execute system tests for various system configurations.
    """

    __TEST_NAME: str = 'test_'
    __CONFIG_PATH: str = CONFIG_PATH
    __TEMP_FILE_ENDING: str = '.test.tmp'
    __LOCAL_CONFIG_EXT: str = '.local.ini'
    __SIMULATION_CONFIG: str = 'simulation'
    __DATA_DIR: str = os.path.join(os.path.dirname(__file__), 'data')
    __CONFIG_EXT: str = '.ini'
    __RESULT_PATH: str = os.path.join(ROOT_PATH, 'results')

    def __init__(self):
        super().__init__(do_simulation=True, do_analysis=True)
        self.__id_generator = self.__get_id_generator()
        self.__tests: [str] = list()

    def _setup_config(self) -> dict:
        # test set for config setup
        self.__rename_local_config()
        configs: dict = dict()
        self.__add(ConfigParser(), configs)
        for file in os.listdir(self.__DATA_DIR):
            if file.endswith(self.__CONFIG_EXT):
                config: ConfigParser = ConfigParser()
                config.read(os.path.join(self.__DATA_DIR, file))
                self.__add(config, configs)
        return configs

    def __add(self, config: ConfigParser, configs: dict) -> None:
        test_id: str = next(self.__id_generator)
        self.__tests.append(test_id)
        configs[test_id] = config

    def __get_id_generator(self) -> str:
        test_id: int = 1
        while True:
            yield self.__TEST_NAME + str(test_id)
            test_id += 1

    def __rename_local_config(self):
        self.__rename_local_simulation_config(self.__LOCAL_CONFIG_EXT, self.__TEMP_FILE_ENDING)

    def __reverse_local_config(self):
        self.__rename_local_simulation_config(self.__TEMP_FILE_ENDING, self.__LOCAL_CONFIG_EXT)

    def __rename_local_simulation_config(self, src_ext: str, dest_ext: str) -> None:
        # 1) Only the simulation.local.ini needs to be renamed.
        # 2) It is safer to copy a file instead of moving or renaming it.
        # 3) Only one place for logic.
        file: str = os.path.join(self.__CONFIG_PATH, self.__SIMULATION_CONFIG + src_ext)
        new_file: str = file.replace(src_ext, dest_ext)
        if os.path.exists(file):
            shutil.copy(file, new_file)
            remove_file(file)
        # for file in os.listdir(self.__CONFIG_PATH):
        #     if file.endswith(self.__LOCAL_CONFIG_EXT):
        #         new_file = file.replace(self.__LOCAL_CONFIG_EXT, self.__TEMP_FILE_ENDING)
        #         os.rename(os.path.join(self.__CONFIG_PATH, file), os.path.join(self.__CONFIG_PATH, new_file))

    # def __rename_local_configs_reverse(self) -> None:
    #     for file in os.listdir(self.__CONFIG_PATH):
    #         if file.endswith(self.__TEMP_FILE_ENDING):
    #             new_file = file.replace(self.__TEMP_FILE_ENDING, self.__LOCAL_CONFIG_EXT)
    #             os.rename(os.path.join(self.__CONFIG_PATH, file), os.path.join(self.__CONFIG_PATH, new_file))

    def clean_up(self) -> None:
        self.__reverse_local_config()
        for test in self.__tests:
            while True:
                try:
                    shutil.rmtree(os.path.join(self.__RESULT_PATH, test))
                    break
                except FileNotFoundError:
                    break
                except PermissionError:
                    print('Waiting for simulation to finish...')
                    time.sleep(1)


if __name__ == "__main__":
    batch_processing: BatchProcessing = TestBatchProcessing()
    try:
        batch_processing.run()
    finally:
        batch_processing.clean_up()
        print('System tests Finished')
