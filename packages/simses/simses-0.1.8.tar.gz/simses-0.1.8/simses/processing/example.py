from configparser import ConfigParser

from simses.processing.batch_processing import BatchProcessing


class ExampleBatchProcessing(BatchProcessing):

    """
    This is just a simple example on how to use BatchProcessing. In principle, it is only needed to setup several configs
    and run it.
    """

    def __init__(self):
        super().__init__(do_simulation=True, do_analysis=True)

    def _setup_config(self) -> dict:
        # Example for config setup
        storage_1: str = 'system_1,no_loss,storage_1\n'
        storage_2: str = 'system_1,no_loss,storage_2\n'
        storage_3: str = 'system_1,no_loss,storage_3\n'
        storage_4: str = 'system_1,no_loss,storage_4\n'
        config_set: dict = dict()
        config_set['storage_1'] = storage_1
        config_set['storage_2'] = storage_2
        config_set['storage_3'] = storage_3
        config_set['storage_4'] = storage_4
        config_set['hybrid_1'] = storage_1 + storage_2
        config_set['hybrid_2'] = storage_3 + storage_4
        configs: dict = dict()
        for name, value in config_set.items():
            config: ConfigParser = ConfigParser()
            config.add_section('STORAGE_SYSTEM')
            config.set('STORAGE_SYSTEM', 'STORAGE_SYSTEM_DC', value)
            configs[name] = config
        return configs

    def clean_up(self) -> None:
        pass


if __name__ == "__main__":
    batch_processing: BatchProcessing = ExampleBatchProcessing()
    batch_processing.run()
    batch_processing.clean_up()
