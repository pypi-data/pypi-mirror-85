from simses.commons.state.technology.storage_technology_state import StorageTechnologyState


class HydrogenStateOld(StorageTechnologyState):
    """
    Current physical state of the hydrogen storage components with the main electrical parameters.
    """

    SYSTEM_AC_ID = 'StorageSystemAC'
    SYSTEM_DC_ID = 'StorageSystemDC'
    SOC = 'SOC in p.u.'
    VOLTAGE = 'voltage of hydrogen system in V'
    VOLTAGE_EL = 'voltage of electrolyzer in V'  # voltage of electrolyzer
    VOLTAGE_FC = 'voltage of fuel cell in V'  # voltage of fuel_cell
    CURRENT = 'current of hydrogen storage system in A'
    CURRENT_EL = 'current of electrolyzer in A'  # current of electrolyzer
    CURRENT_DENSITY_EL = 'current density of electrolyzer in A'
    CURRENT_FC = 'current of fuelcell in A'
    CAPACITY = 'capacity in Wh'
    POWER = 'power in W'
    TEMPERATURE = 'temperature in K'
    TEMPERATURE_EL = 'temperature of electrolyzer stack in Celcius'
    TEMPERATURE_FC = 'temperature of fuelcell stack in Celsius'
    POWER_LOSS = 'Power loss in W'
    HYDROGEN_PRODUCTION = 'hydrogen production in mol/s'  # hydrogen production of electrolyzerstack
    HYDROGEN_OUTFLOW = 'hydrogen outlfow in mol/s'  # hydrogen outflow after pressure controll valve
    HYDROGEN_USE = 'hydrogen use in mol/s'  # hydrogen use of fuel cell
    HYDROGEN_INFLOW = 'hydrogen inflow in mol/s'  # hydrogen inflow into fuelcell stack for pressure control
    OXYGEN_PRODUCTION = 'oxygen production in mol/s'  # oxygen production of electrolyzer
    OXYGEN_OUTFLOW = 'oxygen outflow in mol/s'  # oxygen outflow out of the electrolyzer after pressure control
    OXYGEN_USE = 'oxygen use in mol/s'  # oxygen use of fuel cell
    OXYGEN_INFLOW = 'oxygen inflow in mol/s'  # oxygen inflow into fuelcell stack for pressure control of fuel cell
    FULFILLMENT = 'fulfillment in p.u.'  # ??
    CONVECTION_HEAT = 'convection heat in W'
    TANK_PRESSURE = 'tank pressure in bar'
    # VOLTAGE_OC_EC = 'U_oc_ec in V'
    # VOLTAGE_OC_FC = 'U_oc_fc in V'
    PRESSURE_ANODE_EL = 'relative anode pressure of electrolyzer in barg'
    PRESSURE_CATHODE_EL = 'relative cathode pressure or electrolyzer in barg'
    PRESSURE_ANODE_FC = 'relative anode pressure of fuelcell in barg'
    PRESSURE_CATHODE_FC = 'relative cathode pressure of fuelcell in barg'
    PART_PRESSURE_H2_EL = 'partial pressure H2 in bar'
    PART_PRESSURE_O2_EL = 'partial pressure O2 in bar'
    SAT_PRESSURE_H2O_EL = 'saturation pressure H2O in bar'
    WATER_USE = 'wateruse in mol/s'  # water the electrolyzer splits into hydrogen and oxygen
    WATER_OUTFLOW_CATHODE_EL = 'watersteam outflow cathode electrolyzer in mol/s'
    WATER_OUTFLOW_ANODE_EL = 'watersteam outflow anode electrolyzer in mol/s'
    WATER_FLOW_EL = 'waterflow electrolyzer in mol/s'  # water the is circulated through the EL stack in order to tempering
    POWER_WATER_HEATING_EL  = 'power water heating electrolyzer in W'  # power that is transported by the water stream through the electrolyzer stack
                                                                        # if Ph20 > 0: heating  if Ph2o < 0: heat is transported out of the stack and realeased to the ambient atmosphere (no electrical power needed)
    POWER_PUMP_EL = 'power water circulation electrolyzer in W'  # power the pump consumes for circulation of water through electrolyzer
    POWER_GAS_DRYING = 'power for drying of hydrogen in W'
    POWER_COMPRESSOR = 'power for compression of hydrogen in W'
    TOTAL_HYDROGEN_PRODUCTION = 'total amount of produced hydrogen in kg'
    RESISTANCE_INCREASE_CYCLIC_EL = 'increase resistance cyclic in p.u.'
    RESISTANCE_INCREASE_CALENDAR_EL = 'increase reisistance calendric in p.u.'
    RESISTANCE_INCREASE_EL = 'increase R total in p.u.'
    REFERENCE_VOLTAGE_EL = 'reverence voltage in V'
    EXCHANGE_CURRENT_DENS_DECREASE_CYCLIC_EL = 'decrease j0 cyclic in p.u.'
    EXCHANGE_CURRENT_DENS_DECREASE_CALENDAR_EL = 'decrease j0 calendric in p.u.'
    EXCHANGE_CURRENT_DENS_DECREASE_EL = 'decrease j0 in p.u.'
    SOH_EL = 'SOH electrolyzer in p.u.'

    def __init__(self, system_id: int, storage_id: int):
        super().__init__()
        self._initialize()
        self.set(self.SYSTEM_AC_ID, system_id)
        self.set(self.SYSTEM_DC_ID, storage_id)

    @property
    def soc(self) -> float:
        return self.get(self.SOC)

    @soc.setter
    def soc(self, value: float) -> None:
        self.set(self.SOC, value)

    @property
    def capacity(self) -> float:
        return self.get(self.CAPACITY)

    @capacity.setter
    def capacity(self, value: float):
        self.set(self.CAPACITY, value)

    @property
    def voltage(self) -> float:
        return self.get(self.VOLTAGE)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.set(self.VOLTAGE, value)

    @property
    def voltage_el(self) -> float:
        return self.get(self.VOLTAGE_EL)

    @voltage_el.setter
    def voltage_el(self, value: float) -> None:
        self.set(self.VOLTAGE_EL, value)

    @property
    def voltage_fc(self) -> float:
        return self.get(self.VOLTAGE_FC)

    @voltage_fc.setter
    def voltage_fc(self, value: float) -> None:
        self.set(self.VOLTAGE_FC, value)

    @property
    def current(self) -> float:
        return self.get(self.CURRENT)

    @current.setter
    def current(self, value: float) -> None:
        self.set(self.CURRENT, value)

    @property
    def current_el(self) -> float:
        return self.get(self.CURRENT_EL)

    @current_el.setter
    def current_el(self, value: float) -> None:
        self.set(self.CURRENT_EL, value)

    @property
    def current_density_el(self) -> float:
        return self.get(self.CURRENT_DENSITY_EL)

    @current_density_el.setter
    def current_density_el(self, value: float) -> None:
        self.set(self.CURRENT_DENSITY_EL, value)

    @property
    def current_fc(self) -> float:
        return self.get(self.CURRENT_FC)

    @current_fc.setter
    def current_fc(self, value: float) -> None:
        self.set(self.CURRENT_FC, value)

    @property
    def temperature(self) -> float:
        return self.get(self.TEMPERATURE)

    @temperature.setter
    def temperature(self, value: float) -> None:
        self.set(self.TEMPERATURE, value)

    @property
    def temperature_el(self) -> float:
        return self.get(self.TEMPERATURE_EL)

    @temperature_el.setter
    def temperature_el(self, value: float) -> None:
        self.set(self.TEMPERATURE_EL, value)

    @property
    def temperature_fc(self) -> float:
        return self.get(self.TEMPERATURE_FC)

    @temperature_fc.setter
    def temperature_fc(self, value: float) -> None:
        self.set(self.TEMPERATURE_FC, value)

    @property
    def power_loss(self) -> float:
        return self.get(self.POWER_LOSS)

    @power_loss.setter
    def power_loss(self, value: float) -> None:
        self.set(self.POWER_LOSS, value)

    @property
    def power(self) -> float:
        return self.get(self.POWER)

    @power.setter
    def power(self, value: float) -> None:
        self.set(self.POWER, value)

    @property
    def hydrogen_production(self) -> float:
        return self.get(self.HYDROGEN_PRODUCTION)

    @hydrogen_production.setter
    def hydrogen_production(self, value: float) -> None:
        self.set(self.HYDROGEN_PRODUCTION, value)


    @property
    def hydrogen_outflow(self) -> float:
        return self.get(self.HYDROGEN_OUTFLOW)

    @hydrogen_outflow.setter
    def hydrogen_outflow(self, value: float) -> None:
        self.set(self.HYDROGEN_OUTFLOW, value)

    @property
    def hydrogen_use(self) -> float:
        return self.get(self.HYDROGEN_USE)

    @hydrogen_use.setter
    def hydrogen_use(self, value: float) -> None:
        self.set(self.HYDROGEN_USE, value)

    @property
    def hydrogen_inflow(self) -> float:
        return self.get(self.HYDROGEN_INFLOW)

    @hydrogen_inflow.setter
    def hydrogen_inflow(self, value: float) -> None:
        self.set(self.HYDROGEN_INFLOW, value)

    @property
    def oxygen_production(self) -> float:
        return self.get(self.OXYGEN_PRODUCTION)

    @oxygen_production.setter
    def oxygen_production(self, value: float) -> None:
        self.set(self.OXYGEN_PRODUCTION, value)

    @property
    def oxygen_outflow(self) -> float:
        return self.get(self.OXYGEN_OUTFLOW)

    @oxygen_outflow.setter
    def oxygen_outflow(self, value: float) -> None:
        self.set(self.OXYGEN_OUTFLOW, value)

    @property
    def oxygen_use(self) -> float:
        return self.get(self.OXYGEN_USE)

    @oxygen_use.setter
    def oxygen_use(self, value: float) -> None:
        self.set(self.OXYGEN_USE, value)

    @property
    def oxygen_inflow(self) -> float:
        return self.get(self.OXYGEN_INFLOW)

    @oxygen_inflow.setter
    def oxygen_inflow(self, value: float) -> None:
        self.set(self.OXYGEN_INFLOW, value)

    @property
    def tank_pressure(self) -> float:
        return self.get(self.TANK_PRESSURE)

    @tank_pressure.setter
    def tank_pressure(self, value: float) -> None:
        self.set(self.TANK_PRESSURE, value)

    # @property
    # def voltage_oc_ec(self) -> float:
    #     return self.get(self.VOLTAGE_OC_EC)
    #
    # @voltage_oc_ec.setter
    # def voltage_oc_ec(self, value: float) -> None:
    #     self.set(self.VOLTAGE_OC_EC, value)
    #
    # @property
    # def voltage_oc_fc(self) -> float:
    #     return self.get(self.VOLTAGE_OC_FC)
    #
    # @voltage_oc_fc.setter
    # def voltage_oc_fc(self, value: float) -> None:
    #     self.set(self.VOLTAGE_OC_FC, value)

    @property
    def convection_heat(self) -> float:
        return self.get(self.CONVECTION_HEAT)

    @convection_heat.setter
    def convection_heat(self, value: float) -> None:
        self.set(self.CONVECTION_HEAT, value)

    @property
    def fulfillment(self) -> float:
        return self.get(self.FULFILLMENT)

    @fulfillment.setter
    def fulfillment(self, value: float):
        self.set(self.FULFILLMENT, value)

    @property
    def pressure_anode_el(self) -> float:
        return self.get(self.PRESSURE_ANODE_EL)

    @pressure_anode_el.setter
    def pressure_anode_el(self, value: float):
        self.set(self.PRESSURE_ANODE_EL, value)

    @property
    def pressure_cathode_el(self) -> float:
        return self.get(self.PRESSURE_CATHODE_EL)

    @pressure_cathode_el.setter
    def pressure_cathode_el(self, value: float):
        self.set(self.PRESSURE_CATHODE_EL, value)

    @property
    def pressure_anode_fc(self) -> float:
        return self.get(self.PRESSURE_ANODE_FC)

    @pressure_anode_fc.setter
    def pressure_anode_fc(self, value: float):
        self.set(self.PRESSURE_ANODE_EL, value)

    @property
    def pressure_cathode_fc(self) -> float:
        return self.get(self.PRESSURE_CATHODE_FC)

    @pressure_cathode_fc.setter
    def pressure_cathode_fc(self, value: float):
        self.set(self.PRESSURE_CATHODE_FC, value)

    @property
    def part_pressure_h2_el(self) -> float:
        return self.get(self.PART_PRESSURE_H2_EL)

    @part_pressure_h2_el.setter
    def part_pressure_h2_el(self, value: float):
        self.set(self.PART_PRESSURE_H2_EL, value)

    @property
    def part_pressure_o2_el(self) -> float:
        return self.get(self.PART_PRESSURE_O2_EL)

    @part_pressure_o2_el.setter
    def part_pressure_o2_el(self, value: float):
        self.set(self.PART_PRESSURE_O2_EL, value)

    @property
    def sat_pressure_h2o_el(self) -> float:
        return self.get(self.SAT_PRESSURE_H2O_EL)

    @sat_pressure_h2o_el.setter
    def sat_pressure_h2o_el(self, value: float):
        self.set(self.SAT_PRESSURE_H2O_EL, value)

    @property
    def water_use(self) -> float:
        return self.get(self.WATER_USE)

    @water_use.setter
    def water_use(self, value: float):
        self.set(self.WATER_USE, value)

    @property
    def water_outflow_cathode_el(self) -> float:
        return self.get(self.WATER_OUTFLOW_CATHODE_EL)

    @water_outflow_cathode_el.setter
    def water_outflow_cathode_el(self, value: float):
        self.set(self.WATER_OUTFLOW_CATHODE_EL, value)

    @property
    def water_outflow_anode_el(self) -> float:
        return self.get(self.WATER_OUTFLOW_ANODE_EL)

    @water_outflow_anode_el.setter
    def water_outflow_anode_el(self, value: float):
        self.set(self.WATER_OUTFLOW_ANODE_EL, value)

    @property
    def water_flow_el(self) -> float:
        return self.get(self.WATER_FLOW_EL)

    @water_flow_el.setter
    def water_flow_el(self, value: float):
        self.set(self.WATER_FLOW_EL, value)

    @property
    def power_water_heating_el(self) -> float:
        return self.get(self.POWER_WATER_HEATING_EL)

    @power_water_heating_el.setter
    def power_water_heating_el(self, value: float):
        self.set(self.POWER_WATER_HEATING_EL, value)

    @property
    def power_pump_el(self) -> float:
        return self.get(self.POWER_PUMP_EL)

    @power_pump_el.setter
    def power_pump_el(self, value: float):
        self.set(self.POWER_PUMP_EL, value)

    @property
    def power_gas_drying(self) -> float:
        return self.get(self.POWER_GAS_DRYING)

    @power_gas_drying.setter
    def power_gas_drying(self, value: float):
        self.set(self.POWER_GAS_DRYING, value)

    @property
    def power_compressor(self) -> float:
        return self.get(self.POWER_COMPRESSOR)

    @power_compressor.setter
    def power_compressor(self, value: float):
        self.set(self.POWER_COMPRESSOR, value)

    @property
    def total_hydrogen_production(self) -> float:
        return self.get(self.TOTAL_HYDROGEN_PRODUCTION)

    @total_hydrogen_production.setter
    def total_hydrogen_production(self, value: float):
        self.set(self.TOTAL_HYDROGEN_PRODUCTION, value)

    @property
    def resistance_increase_cyclic_el(self) -> float:
        return self.get(self.RESISTANCE_INCREASE_CYCLIC_EL)

    @resistance_increase_cyclic_el.setter
    def resistance_increase_cyclic_el(self, value: float):
        self.set(self.RESISTANCE_INCREASE_CYCLIC_EL, value)

    @property
    def resistance_increase_calendar_el(self) -> float:
        return self.get(self.RESISTANCE_INCREASE_CALENDAR_EL)

    @resistance_increase_calendar_el.setter
    def resistance_increase_calendar_el(self, value: float):
        self.set(self.RESISTANCE_INCREASE_CALENDAR_EL, value)

    @property
    def resistance_increase_el(self) -> float:
        return self.get(self.RESISTANCE_INCREASE_EL)

    @resistance_increase_el.setter
    def resistance_increase_el(self, value: float):
        self.set(self.RESISTANCE_INCREASE_EL, value)

    @property
    def reference_voltage_el(self) -> float:
        return self.get(self.REFERENCE_VOLTAGE_EL)

    @reference_voltage_el.setter
    def reference_voltage_el(self, value: float):
        self.set(self.REFERENCE_VOLTAGE_EL, value)

    @property
    def exchange_current_decrease_cyclic_el(self) -> float:
        return self.get(self.EXCHANGE_CURRENT_DENS_DECREASE_CYCLIC_EL)

    @exchange_current_decrease_cyclic_el.setter
    def exchange_current_decrease_cyclic_el(self, value: float):
        self.set(self.EXCHANGE_CURRENT_DENS_DECREASE_CYCLIC_EL, value)

    @property
    def exchange_current_decrease_calendar_el(self) -> float:
        return self.get(self.EXCHANGE_CURRENT_DENS_DECREASE_CALENDAR_EL)

    @exchange_current_decrease_calendar_el.setter
    def exchange_current_decrease_calendar_el(self, value: float):
        self.set(self.EXCHANGE_CURRENT_DENS_DECREASE_CALENDAR_EL, value)

    @property
    def exchange_current_decrease_el(self) -> float:
        return self.get(self.EXCHANGE_CURRENT_DENS_DECREASE_EL)

    @exchange_current_decrease_el.setter
    def exchange_current_decrease_el(self, value: float):
        self.set(self.EXCHANGE_CURRENT_DENS_DECREASE_EL, value)

    @property
    def soh_el(self) -> float:
        return self.get(self.SOH_EL)

    @soh_el.setter
    def soh_el(self, value: float):
        self.set(self.SOH_EL, value)

    @property
    def id(self) -> str:
        return 'HYDROGEN' + str(self.get(self.SYSTEM_AC_ID)) + str(self.get(self.SYSTEM_DC_ID))

    @property
    def is_charge(self) -> bool:
        return self.power > 0

    @classmethod
    def sum_parallel(cls, hydrogen_states: []):
        hydrogen_state = HydrogenState(0, 0)
        return hydrogen_state

    @classmethod
    def sum_serial(cls, states: []):
        pass