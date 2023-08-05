import pandas as pd


class DataImport:

    def __init__(self, result_directory: str, state_cls):
        raise Exception('DEPRECATED')
        self.__filename: str = result_directory + '/' + state_cls.__name__ + '.csv'
        self.__data: pd.DataFrame = pd.read_csv(self.__filename, sep=',', header=0)
        # print('==== ' + state_cls.__name__ + ' ====')
        for key in self.__data.keys():
            self.__data[key] = pd.to_numeric(self.__data[key], errors='coerce')
        # self.__data = self.__data.replace(np.nan, 0, regex=True)
        # print(self.__data.dtypes)

    def return_data(self) -> pd.DataFrame:
        """
        Function to let the DataExport Thread know that the simulation is done and stop after emptying the queue.

        Parameters
        ----------

        Returns
        -------
        pandas DataFrame
            Returns the required data in pandas dataframe format

        """
        return self.__data

    # @staticmethod
    # def types_dict_of(state) -> dict:
    #     """
    #
    #     Parameters
    #     ----------
    #     state :
    #
    #     Returns
    #     -------
    #     dict
    #
    #
    #     """
    #     header_map = {0: np.float64}
    #     for h in state.header():
    #         header_map[h] = np.float64
    #     return header_map
