# Computes the (n+1)st Fibonacci number ieteratively and recursively.
#
# Written by Eric Martin for COMP9021


def iterative_fibonacci(n):
    if n < 2:
        return n
    previous, current = 0, 1
    for i in range(2, n + 1):
        previous, current = current, previous + current
    return current # previous => current => previous + current      

def recursive_fibonacci(n):
    if n >= 2:
        return recursive_fibonacci(n - 2) + recursive_fibonacci(n - 1)
    return n


if __name__ == '__main__':
    print('Generating the first 40 nonzero Fibonacci numbers:')
    for n in range(1, 41):
        print(iterative_fibonacci(n), end = ' ')
        if n % 10 == 0:
            print()
    print()
    print('Generating the first 40 nonzero Fibonacci numbers recursively up to 40:')
    for n in range(1, 41):
        print(recursive_fibonacci(n), end = ' ')
        if n % 10 == 0:
            print()

