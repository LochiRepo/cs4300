#Testing the Arith functions
import task2

#Test integer by calling the values starting with integer
def test_integer():
    values = task2.getVal()
    assert isinstance(values[0], int)

#Each assert tests an instance for datate type
def test_float():
    values = task2.getVal()
    assert isinstance(values[1], float)

#Test string
def test_string():
    values = task2.getVal()
    assert isinstance(values[2], str)

#Tests a Boolean
def test_boolean():
    values = task2.getVal()
    assert isinstance(values[3], bool)

#Tests Float Arith
def test_arithmetic():
    values = task2.getVal()
    assert values[4] == 2.0 / 3.0
