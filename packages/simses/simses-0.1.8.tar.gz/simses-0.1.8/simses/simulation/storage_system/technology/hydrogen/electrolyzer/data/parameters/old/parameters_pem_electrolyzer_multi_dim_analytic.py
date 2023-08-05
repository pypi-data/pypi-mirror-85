import pandas as pd

from simses.config.data.electrolyzer_data_config import ElectrolyzerDataConfig
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.data.parameters.parameters import Parameters


class ParametersPemElectrolyzerMultiDimAnalytic(Parameters):
    def __init__(self, electrolyzer_data_config: ElectrolyzerDataConfig):
        super().__init__()
        self.__PARA_FILE = electrolyzer_data_config.pem_electrolyzer_multi_dim_analytic_para_file
        self.corr_parameters = list()
        self.import_parameters()

        # parameters of quadratic regression of activation powerdensity
        self.__p00 = 0.01365
        self.__p10 = 0.4712
        self.__p01 = -0.0008169
        self.__p20 = 0.01156
        self.__p11 = -0.001533
        self.__p02 = 8.12 * 10 ** (-6)

    def import_parameters(self) -> None:
        correction_parameters = pd.read_csv(self.__PARA_FILE, delimiter=';', decimal=",")
        self.corr_parameters = correction_parameters.iloc[:, 0]

    def get_corr_parameter_q1(self) -> float:
        return self.corr_parameters[0]

    def get_corr_parameter_q2(self) -> float:
        return self.corr_parameters[1]

    def get_corr_parameter_q3(self) -> float:
        return self.corr_parameters[2]

    def get_corr_parameter_q5(self) -> float:
        return self.corr_parameters[3]

    def get_corr_parameter_q11(self) -> float:
        return self.corr_parameters[4]

    def get_corr_parameter_q12(self) -> float:
        return self.corr_parameters[5]

    def get_corr_parameter_q13(self) -> float:
        return self.corr_parameters[6]

    def get_corr_parameter_q14(self) -> float:
        return self.corr_parameters[7]

    def get_corr_parameter_q15(self) -> float:
        return self.corr_parameters[8]

    def get_corr_parameter_q16(self) -> float:
        return self.corr_parameters[9]

    def get_corr_parameter_q18(self) -> float:
        return self.corr_parameters[10]

    def get_corr_parameter_q20(self) -> float:
        return self.corr_parameters[11]

    def get_corr_parameter_q22(self) -> float:
        return self.corr_parameters[12]

    def get_corr_parameter_q23(self) -> float:
        return self.corr_parameters[13]

    def get_corr_parameter_q24(self) -> float:
        return self.corr_parameters[14]

    def get_corr_parameter_q25(self) -> float:
        return self.corr_parameters[15]

    def get_act_pow_parameter_p00(self) -> float:
        return self.__p00

    def get_act_pow_parameter_p10(self) -> float:
        return self.__p10

    def get_act_pow_parameter_p01(self) -> float:
        return self.__p01

    def get_act_pow_parameter_p20(self) -> float:
        return self.__p20

    def get_act_pow_parameter_p11(self) -> float:
        return self.__p11

    def get_act_pow_parameter_p02(self) -> float:
        return self.__p02