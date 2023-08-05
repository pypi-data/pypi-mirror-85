import pytest  # important to be able to use @pytest...

from simses.config.data.electrolyzer_data_config import ElectrolyzerDataConfig
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.electrolyzer_stack_model import \
    ElectrolyzerStackModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.stack_model.pem_electrolyzer import \
    PemElectrolyzer

"""
Test ideas for Electrolyzers:
- hydrogen Production >=0; 
- hydrogen Production >0 bei power >0
- Pressure anode, cathode >=1


For PEM:
- Pressure anode >= pressure cathode (Differenzdruck über Membran muss >= 0 sein)



"""

'''
#1. Simple Test: Syntax, multiple asserts, import pytest, output in cmd

# def test_propertyof_product():
#     assert demo.product(5,5) == 25 #What should the result be?

#2. Test a Class using pytest's fixtures

# @pytest.fixture(scope="module")#module: gets only one instance
# def make_demo_instance():
#     print("Hey! I got instanciated :)")
#    return Demo()

def test_add(make_demo_instance):
    assert make_demo_instance.add(2, 2) == 4 #quick maths

#3. Parametrize a Test using pytest

@pytest.mark.parametrize('num1, num2, result',
                         [
                             (4, 1, 3),
                             (5, 5, 0)
                         ]
                         )
def test_subtract(num1, num2, result, make_demo_instance):
    print("For debugging reasons it is sometimes nice to print Variables. You can do this with -s", num1)
    assert make_demo_instance.subtract(num1, num2) == result

#4. Practical Example?

#Goto ACDC Example

#5. More Test Types and ressources

#60 Minute Tutorial: https://www.youtube.com/watch?v=bbp_849-RZ4
#Pytest Homepage for examples: https://docs.pytest.org/en/latest/example/index.html
'''


@pytest.fixture(scope="function") #module: gets only one instance
def uut(nominal_power) -> ElectrolyzerStackModel:
    return PemElectrolyzer(nominal_power, ElectrolyzerDataConfig())




@pytest.mark.parametrize('nominal_power, power, temperature, pressure_anode, pressure_cathode, current_result',
                         [
                             (5, 0, 0, 0, 0, 0)
                         ]
                         )
def test_calculate_current(uut, power, temperature, pressure_anode, pressure_cathode, current_result):
    uut.calculate(power, temperature, pressure_anode, pressure_cathode)
    assert uut.get_current() == current_result

@pytest.mark.parametrize('nominal_power, power, temperature, pressure_anode, pressure_cathode, current_result',
                         [
                             (5, 5, 20, 1, 1, 0)
                         ]
                         )
def test_calculate_geq_current(uut, power, temperature, pressure_anode, pressure_cathode, current_result):
    uut.calculate(power, temperature, pressure_anode, pressure_cathode)
    assert uut.get_current() > current_result

@pytest.mark.parametrize('nominal_power, power, temperature, pressure_anode, pressure_cathode, voltage_result',
                         [
                             (10, 10, 25, 1, 1, 0),
                             (10, 0, 25, 0, 0, 0)
                         ]
                         )
def test_calculate_voltage(uut, power, temperature, pressure_anode, pressure_cathode, voltage_result):
    uut.calculate(power, temperature, pressure_anode, pressure_cathode)
    assert uut.get_voltage() > voltage_result

@pytest.mark.parametrize('nominal_power, power, temperature, pressure_anode, pressure_cathode, h2_flow_result',
                         [
                             (10, 10, 25, 1, 1, 0)
                         ]
                         )
def test_calculate_hydrogen_flow_geq(uut, power, temperature, pressure_anode, pressure_cathode, h2_flow_result):
    uut.calculate(power, temperature, pressure_anode, pressure_cathode)
    assert uut.get_hydrogen_production() > h2_flow_result

@pytest.mark.parametrize('nominal_power, power, temperature, pressure_anode, pressure_cathode, h2_flow_result',
                         [
                             (10, 0, 25, 0, 0, 0)
                         ]
                         )
def test_calculate_hydrogen_flow(uut, power, temperature, pressure_anode, pressure_cathode, h2_flow_result):
    uut.calculate(power, temperature, pressure_anode, pressure_cathode)
    assert uut.get_hydrogen_production() == h2_flow_result

@pytest.mark.parametrize('nominal_power, power, temperature, pressure_anode, pressure_cathode, get_water_use_result',
                         [
                             (10, 10, 25, 1, 1, 0)
                         ]
                         )
def test_calculate_water_use(uut, power, temperature, pressure_anode, pressure_cathode, get_water_use_result):
    uut.calculate(power, temperature, pressure_anode, pressure_cathode)
    assert uut.get_water_use() > get_water_use_result



