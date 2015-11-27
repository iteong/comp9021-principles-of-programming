
def nb_of_consecutive_squares(n):
    if not sums_of_two_squares[n]:
        return 0
    if not sums_of_two_squares[n + 1]:
        return 1
    if not sums_of_two_squares[n + 2]:
        return 2
    return 3

# The largest number whose square is a 3-digit number.
max = 31
# For all n in [100, 999], if n is found to be of the form a^2 + b^2
# then sums_of_two_squares[n] will be set to (a, b).
# Note that there might be other decompositions of n into a sum of 2 squares;
# we just recall the first decomposition we find.
# Also note that we waste the 100 first elements of the array;
# we can afford it and this choice makes the program simpler.
sums_of_two_squares = [None] * 1000

for i in range(max + 1):
    for j in range(i, max + 1):
        n = i * i + j * j
        if n < 100:
            continue
        if n >= 1000:
            break
        sums_of_two_squares[n] = (i, j)

for n in range(100, 1000):
    i = nb_of_consecutive_squares(n)
    if i < 3:
        # There is no potential triple before n + i + 1; the loop will increment n by 1.
        n += i;
        continue
    print('({:}, {:}, {:}) '
          '(equal to {:}^2+{:}^2, {:}^2+{:}^2, {:}^2+{:}^2) is a solution.'.format(n, n + 1, n + 2,
           sums_of_two_squares[n][0], sums_of_two_squares[n][1],
           sums_of_two_squares[n + 1][0], sums_of_two_squares[n + 1][1],
           sums_of_two_squares[n + 2][0], sums_of_two_squares[n + 2][1]))
    # We assume we could have two solutions of the form
    # (n, n + 1, n + 2) and (n + 1, n + 2, n + 3)
    # (but as the solution shows, this never happens...),
    # hence n is incremented by only 1 in the next iteration of the loop.
    # We could avoid checking that sums_of_two_squares[n + 1] and
    # sums_of_two_squares[n + 2] are not equal to 0, but why make the program
    # more complicated for no significant gain?

