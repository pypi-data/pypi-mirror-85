

class PowerDistributorStates:
    """
    PowerDistributorStates contains information for SecondLifeHybridPowerDistributor.
    """

    def __init__(self, soh: float, sys_id: int, soc: float):
        """
        Constructor of PowerDistributorStates

        Parameters
        ----------

        soh :
            state of health of a system
        sys_id :
            number of ac or dc system
        soc :
            state of charge of a system
        """

        self.__soh: float = soh
        self.__id: int = sys_id
        self.__soc: float = soc

    @property
    def soh(self) -> float:
        return self.__soh

    @soh.setter
    def soh(self, value: float) -> None:
        self.__soh = value

    @property
    def sys_id(self) -> float:
        return self.__id

    @sys_id.setter
    def sys_id(self, value: float) -> None:
        self.__id = value

    @property
    def soc(self) -> float:
        return self.__soc

    @soc.setter
    def soc(self, value: float) -> None:
        self.__soc = value

    @staticmethod
    def sort_by_soc(data: list, descending: bool = False) -> None:
        """
        In-place sorting of list with PowerDistributorState objects by soc (ascending by default)

        Parameters
        ----------
        descending :
            reverse sorting of data list, default: False
        data :
            list of TimeValue objects

        Returns
        -------

        """
        data.sort(key=lambda x: x.soc, reverse=descending)

    @staticmethod
    def sort_by_soh(data: list, descending: bool = True) -> None:
        """
        In-place sorting of list with PowerDistributorState objects by soh (descending by default)

        Parameters
        ----------
        descending :
            reverse sorting of data list, default: True
        data :
            list of TimeValue objects

        Returns
        -------

        """
        data.sort(key=lambda x: x.soh, reverse=descending)
