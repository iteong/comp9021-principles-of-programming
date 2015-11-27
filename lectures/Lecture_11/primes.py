# Defines a functions to
# - check whether a number is prime,
# - generate a list of prime numbers up to a given number,
# - generate prime numbers one by one,
# - find the prime decomposition of a number
# - find the list of prime decompositons of all numbers up to a given number.
#
# Written by Eric Martin for COMP9021


from math import sqrt


def is_prime(N):
    if N == 2:
        return True
    if N < 2 or N % 2 == 0:
        return False 
    # We let primes_sieve encode the sequence (2, 3, 5, 7, 9, 11, ..., N')
    # with N' equal to N if N is odd and N - 1 is N is even.
    # The index of N' is N_index
    N_index = (N - 1) // 2
    primes_sieve = [True] * (N_index + 1)
    for n in range(1, (round(sqrt(N)) + 1) // 2):
        if primes_sieve[n]:
            if N % (2 * n + 1) == 0:
                return False
            # If n is the index of p then 2 * n * (n + 1) is the index of p ** 2;
            # Also, we increment the value by 2p, which corresponds to increasing the index by 2 * n + 1.
            for i in range(2 * n * (n + 1), N_index + 1, 2 * n + 1):
                primes_sieve[i] = False
    return True


def list_of_primes_up_to(N):
    # We let primes_sieve encode the sequence (2, 3, 5, 7, 9, 11, ..., N')
    # with N' equal to N if N is odd and N - 1 is N is even.
    # The index of N' is N_index
    N_index = (N - 1) // 2
    primes_sieve = [True] * (N_index + 1)
    for n in range(1, (round(sqrt(N)) + 1) // 2):
        if primes_sieve[n]:
            # If n is the index of p then 2 * n * (n + 1) is the index of p ** 2;
            # Also, we increment the value by 2p, which corresponds to increasing the index by 2 * n + 1.
            for i in range(2 * n * (n + 1), N_index + 1, 2 * n + 1):
                primes_sieve[i] = False
    list_of_primes = [2]
    for n in range(1, N_index + 1):
        if primes_sieve[n]:
            list_of_primes.append(2 * n + 1)
    return list_of_primes


def generate_next_prime():
    yield 2
    yield 3
    yield 5
    primes = [5]
    add_two = True
    prime_candidate = 5
    while True:
        # We skip multiples of 2 and multiples of 3, noting that every third odd number is a multiple of 3,
        # and all other multiples of 3 are multiples of 2.
        if add_two:
            prime_candidate += 2
        else:
            prime_candidate += 4
        add_two = not add_two
        j = 0
        while primes[j] * primes[j] <= prime_candidate:
            if prime_candidate % primes[j] == 0:
                break
            j += 1
        else:
            primes.append(prime_candidate)
            yield prime_candidate


def prime_decomposition(N):
    list_of_primes = list_of_primes_up_to(N // 2)
    decomposition = []
    for p in list_of_primes:
        if N % p == 0:
            exp = 1
            while N % p ** (exp + 1) == 0:
                exp += 1
            decomposition.append((p, exp))
    if not decomposition:
        return [(N, 1)]
    return decomposition


def list_of_prime_decompositions_up_to(N):
    decompositions = [False] * (N + 1)
    for i in range(2, N + 1):
        decompositions[i] = {}
    for n in range(2, N + 1):
        if not decompositions[n]:
            # Then n is a prime number.
            exp = 1
            power_of_n = n ** exp
            while power_of_n <= N:
                for i in range(power_of_n, N + 1, power_of_n):
                    decompositions[i][n] = exp
                exp += 1
                power_of_n = n ** exp
    return decompositions

