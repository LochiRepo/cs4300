import task4

#Testing each variation, testing 10% on 100
def test_discount_integers():
    assert task4.calculate_discount(100, 10) == 90

#testing for floats
def test_discount_floats():
    assert task4.calculate_discount(100.0, 15.0) == 85.0

#Testing for values over 100
def test_mixed_types():
    assert task4.calculate_discount(200, 12.5) == 175.0
