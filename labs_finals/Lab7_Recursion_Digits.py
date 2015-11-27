available = int(input('Input available digits: '))
desired = int(input('Input desired sum: '))

def solve(available, desired):
    # if desired sum is negative
    if desired < 0:
        return 0
    # no available digits left after % at each additional level of recursion tree (at bottom of tree)
    if available == 0:
        # base case reached after expanding recursion tree
        if desired == 0:
            return 1
        # base case not reached after expanding recursion tree
        else:
            return 0
    return solve(available // 10, desired) + solve(available // 10, desired - (available % 10))


solutions = solve(available, desired)
if solutions == 0:
    print('There is no solution.')
elif solutions == 1:
    print('There is 1 solution.')
else: # solutions > 1
    print('There are {:} solutions.'.format(solutions))
