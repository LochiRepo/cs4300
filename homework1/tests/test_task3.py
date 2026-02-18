import task3

#Test each variable for if statement on pos/neg/zero
def test_neg_positive():
    assert task3.negTest(5) == "positive"

def test_neg_zero():
    assert task3.negTest(0) == "zero"

def test_neg_negative():
    assert task3.negTest(-3) == "negative"

#Tests the primes to see if they fit
def test_tenPrimes():
    assert task3.tenPrimes() == [2,3,5,7,11,13,17,19,23,29]

#Tests final value for integer adding 1-100
def test_sumHundred():
    assert task3.sumHundred() == 5050
