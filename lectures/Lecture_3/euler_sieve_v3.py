# Generates an initial segment of the list of prime numbers using Euler sieve
# using linked lists.
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
    class Node:
        def __init__(self, number):
            self.number = number
            self.previous = None
            self.next = None

    primes_sieve = [Node(i) for i in range(N + 2)]
    for i in range(2, N + 2):
        primes_sieve[i].previous = primes_sieve[i - 1]
    for i in range(2, N + 1):
        primes_sieve[i].next = primes_sieve[i + 1]   
    i_node = primes_sieve[2]
    i = i_node.number
    while i <= round(sqrt(N)):
        k_node = i_node
        while True:
            factor = i * k_node.number
            if factor > N:
                break
            while factor <= N:
                primes_sieve[factor].next.previous = primes_sieve[factor].previous
                primes_sieve[factor].previous.next = primes_sieve[factor].next
                factor *= i
            k_node = k_node.next
        i_node = i_node.next
        i = i_node.number

    field_width = len(str(N)) + 2
    nb_of_fields = 60 // field_width
    count = 0
    p = primes_sieve[2]
    while p.next:
        print("{0:{1}d}".format(p.number, field_width), end = '')
        count += 1
        if count % nb_of_fields == 0:
            print()
        p = p.next
    if count % nb_of_fields:
        print()


if __name__ == '__main__':
    generate_primes()
