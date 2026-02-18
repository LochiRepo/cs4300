#if block to test for negative numbers
def negTest(x):
    if x > 0:
        return "positive"
    elif x == 0:
        return "zero"
    else:
        return "negative"

#Provide list of first 10 primes
def tenPrimes():
    primes = [2,3,5,7,11,13,17,19,23,29]

    return primes

#This adds the values of k together from 1-100 to 5050
def sumHundred():
    k = 1
    total = 0
    while k <= 100:
        total += k
        k += 1
    return total
