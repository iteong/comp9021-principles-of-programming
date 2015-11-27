# Generates an initial segment of the list of prime numbers using Eratosthenes sieve
# using the most straighforward approach.
#
# Written by Eric Martin for COMP9021

from math import sqrt
from input_int import input_int


def generate_primes():
    print('I will generate all prime numbers in the range [2, N].')
    N = input_int()
    if N < 2:
        return
    primes(N)

    
def primes(N):
    primes_sieve = [True] * (N + 1)
    for n in range(2, round(sqrt(N)) + 1): #when you sqrt 25, it can be 5 or 5.0001,
        # so use round to know exact
        if primes_sieve[n]:
            for i in range(n * n, N + 1, n):
                primes_sieve[i] = False

    field_width = len(str(N)) + 2
    nb_of_fields = 60 // field_width
    count = 0
    for n in range(2, N + 1):
        if primes_sieve[n]:
            print("{0:{1}d}".format(n, field_width), end = '')
            count += 1
            if count % nb_of_fields == 0:
                print()
    if count % nb_of_fields:
        print()
    
    
if __name__ == '__main__':
    generate_primes()
