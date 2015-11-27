# Solves the tower and m glass marbles problem. The user is
# prompted to enter the number n of floors of a building.
# Using m marbles, one has to discover the highest floor,
# if any, such that dropping a marble from that floor makes
# it break, using a strategy that minimises the number of
# drops in the worst case (it is assumed that any marble would
# break when dropped from a floor where one marble breaks, and
# also when dropped from any higher floor; the marbles might
# not break when dropped from any floor).
#
# The idea is to ask: what is the maximum height h of a building
# such that an answer can always be found with no more than d
# drops? Let H(d, m) denote that maximum height.
# - If the marble breaks, m - 1 marbles remain and no higher floor needs to be tested.
# - If the marble does not break, m marbles remain and no lower floor needs to be tested.
# - In any case, d - 1 drops remain.
# This yields: H(d, m) = H(d - 1, m - 1) + H(d - 1, m) + 1.
# The base cases are when either d = 0 or m = 0, in which case H(d, m) = 0.
# This allows one to compute d as the least integer with H(d, m) >= n.
# For the simulation, if low is the highest floor from which
# it is known that a marble can be dropped without breaking,
# d' is the number of drops that remain, and m' is the number
# of marbles that remain, then the next marble should be dropped
# from floor low + H(d' - 1, m' - 1) + 1.
#
# Set B(0, k) = 1 for all k, B(n, 0) = 1 for all n, and
# B(n + 1, k + 1) = B(n, k) + B(n, k + 1).
# The recurrence relation is identical to the one that
# determines the binomial coefficients.
# It is easy to verify that:
# - H(n, k) is equal to B(n, k) - 1;
# - if k > n then B(n, k) is equal to B(n, n);
# - if k <= n then B(n, k) is equal to the sum of n choose k1
# where k1 ranges over {0, ..., k}.
# The values B(n, k) determine the Bernouilli rectangle,
# whose rows are computed similarly to the rows of
# Pascal triangle. The program makes direct use of B(., .),
# and indirect use of H(., .):
#
# 0  1  2  3  4  5  6       
#  --- nb of marbles  --->
# 1  1  1  1  1  1  1  ...  |     0
# 1  2  2  2  2  2  2  ...  nb    1
# 1  3  4  4  4  4  4  ...  of    2
# 1  4  7  8  8  8  8 ...   drops 3
# 1  5 11 15 16 16 16 ...   |     4
# 1  6 16 26 31 32 32 ...   |     5
# ........................  V
#
# Written by Eric Martin for COMP9021


from random import randint


# Computes the first k + 1 elements of the (n + 1)-st row of Bernouilli rectangle
def bernouilli_row_up_to(n, k):
    row = [1] * (k + 1)
    if k == 0:
        return
    for m in range(1, n + 1):
        bernouilli_change_to_next_row_up_to(m, k, row)
    return row   

# Changes the first k + 1 elements of the n-th row of Bernouilli rectangle
# to the first k + 1 elements of the (n + 1)-st row.
def bernouilli_change_to_next_row_up_to(n, k, row):
    min_n_k = min(n, k)
    first_term = 1
    for i in range(1, min_n_k + 1):
        second_term = row[i]
        row[i] += first_term
        first_term = second_term
    for i in range(n + 1, k + 1):
        row[i] = row[min_n_k]

# Compute the first k + 1 elements of the (n + 1)-st row of Bernouilli rectangle
# from the first k + 1 elements of the n-th row
# row[1] is assumed to have been set to 1.
def bernouilli_next_row_up_to(n, k, row, previous_row):
    if k == 0:
        return
    min_n_k = min(n, k)
    for i in range(1, min_n_k + 1):
        row[i] = previous_row[i - 1] + previous_row[i]
    for i in range(n + 1, k + 1):
        row[i] = row[min_n_k]

# Computes the least d with H(d, m) >= n,
# taking advantage of the fact that when k >= i, H(i, k) = B(i, k) - 1 = 2^i - 1.
def nb_of_drops_needed(n, m):
    d = 1
    height = 1
    while height < n:
        d += 1
        if d > m:
            break
        height = 2 ** d - 1
    if height >= n:
        return d
    bernouilli_row = bernouilli_row_up_to(d, m)
    while bernouilli_row[m] - 1 < n:
        d += 1
        bernouilli_change_to_next_row_up_to(d, m, bernouilli_row)
    return d
        
while True:
    # The n from the program description.
    n = input('Enter the number of floors (a strictly positive number): ')
    try:
        n = int(n)
        if n <= 0:
            raise Exception
        break
    except:
        print('Incorrect input, try again.')
while True:
    # The m from the program description.
    m = input('Enter the number of marbles (a strictly positive number): ')
    try:
        m = int(m)
        if m <= 0:
            raise Exception
        break
    except:
        print('Incorrect input, try again.')

# The d from the program description.
d = nb_of_drops_needed(n, m)
if d == 1:
   print('At most 1 drop will be needed.\n')
else:
   print('At most {:} drops will be needed.\n'.format(d))

# Compute and store B(i, k) for all i in {0, ..., d - 1} and k in {0, ..., m - 1}.
bernouilli_rows = [[1] * (m + 1) for i in range(d + 1)]
for i in range(1, d):
   bernouilli_next_row_up_to(i, m - 1, bernouilli_rows[i], bernouilli_rows[i - 1])
# The highest floor such that it is known that a marble dropped from that floor does not break.
low = 0
# The smallest floor such that it is known that a marble dropped from that floor breaks
# (it is convenient to assume that a glass dropped from a level one more  than the height of the building breaks).
high = n + 1
drop = 0
marble = 1
# We randomly make marbles break on one of floors 1, 2, ..., n + 1
# (in case the value is n + 1, the marble does not break when dropped from any floor of the building).
breaking_floor = randint(1, n + 1)
while low < high - 1:
    d -= 1
    floor = min(low + bernouilli_rows[d][m - 1], high - 1)
    drop += 1
    if breaking_floor <= floor:
       print('Drop #{:} with marble #{:}, from floor {:}... marble breaks!'.format(drop, marble, floor))
       marble += 1
       high = floor
       m -= 1
    else:
       print('Drop #{:} with marble #{:}, from floor {:}... marble does not break!'.format(drop, marble, floor))
       low = floor


