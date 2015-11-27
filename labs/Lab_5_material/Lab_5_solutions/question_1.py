# Description: Generates all 3 x 3 magic squares.
#
# Essentially written by Pang Luo for COMP9021

# The sum of each row, column and diagonal is necessarily equal to
# ((1 + 9) * 9 / 2) / 3 = 15.
# Denoting by c the value of the cell at the centre,
# adding up the two diagonals, the middle row and the middle column yields
# 15 * 4 = 45 + 3c, hence c = 5.

all_nonzero_digits = set(range(1, 10))
for a in range(1, 10):
    for b in range(1, 10):
        candidate = (a        , 15 - a - b, b        ,
                     5 + b - a, 5         , 5 + a - b,
                     10 - b   , a + b - 5 , 10 - a   )
        if set(candidate) == all_nonzero_digits:
            print('  {:}  {:}  {:}\n  {:}  {:}  {:}\n  {:}  {:}  {:}\n'.format(*candidate))
