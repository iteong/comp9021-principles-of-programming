# Generates an initial segment of the list of prime numbers using Eratosthenes sieve
# without encoding the even numbers greater than 2.
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
    # We let primes_sieve encode the sequence (2, 3, 5, 7, 9, 11, ..., N')
    # with N' equal to N if N is odd and N - 1 is N is even.
    # The index of N' is N_index
    N_index = (N - 1) // 2
    primes_sieve = [True] * (N_index + 1)
    for k in range(1, (round(sqrt(N)) + 1) // 2):
        if primes_sieve[k]:
            # If k is the index of n then 2 * k * (k + 1) is the index of n ** 2;
            # Also, we increment the value by 2n, which corresponds to increasing the index by 2 * k + 1.
            for i in range(2 * k * (k + 1), N_index + 1, 2 * k + 1):
                primes_sieve[i] = False

    field_width = len(str(N)) + 2
    print("{0:{1}d}".format(2, field_width), end = '')
    nb_of_fields = 60 // field_width
    count = 1
    for n in range(1, N_index + 1):
        if primes_sieve[n]:
            print("{0:{1}d}".format(2 * n + 1, field_width), end = '')
            count += 1
            if count % nb_of_fields == 0:
                print()
    if count % nb_of_fields:
        print()


if __name__ == '__main__':
    generate_primes()
