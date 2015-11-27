# Generates an initial segment of the list of prime numbers using Sundaram sieve.
#
# Written by Eric Martin for COMP9021


from input_int import input_int
from math import ceil


def generate_primes():
    print('I will generate all prime numbers in the range [2, N].')
    N = input_int()
    if N < 2:
        return
    primes(N)

    
def primes(N):
    half_N = (N + 1) // 2
    half_primes_sieve = [True] * half_N
    for i in range(1, half_N):
        for j in range(i, ceil((half_N - i) / (1 + 2 * i))):
            half_primes_sieve[i + j + 2 * i * j] = False

    field_width = len(str(N)) + 2
    print("{0:{1}d}".format(2, field_width), end = '')
    nb_of_fields = 60 // field_width
    count = 1
    for n in range(1, half_N):
        if half_primes_sieve[n]:
            print("{0:{1}d}".format(2 * n + 1, field_width), end = '')
            count += 1
            if count % nb_of_fields == 0:
                print()
    if count % nb_of_fields:
        print()


if __name__ == '__main__':
    generate_primes()
