# Generates an initial segment of the list of prime numbers using Euler sieve
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
    primes_sieve = list(range(2, N + 1))
    i = 0
    while primes_sieve[i] <= round(sqrt(N)):
        k = 0
        while True:
            factor = primes_sieve[i] * primes_sieve[i + k]
            if factor > N:
                break
            while factor <= N:
                primes_sieve.remove(factor)
                factor *= primes_sieve[i]
            k += 1
        i += 1

    field_width = len(str(N)) + 2
    nb_of_fields = 60 // field_width
    count = 0
    for n in primes_sieve:
        print("{0:{1}d}".format(n, field_width), end = '')
        count += 1
        if count % nb_of_fields == 0:
            print()
    if count % nb_of_fields:
        print()


if __name__ == '__main__':
    generate_primes()
