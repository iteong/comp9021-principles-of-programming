# Prompts the user for two numbers, say available_digits and desired_sum, and
# outputs the number of ways of selecting digits from available_digits
# that sum up to desired_sum.
#
# Written by Eric Martin for COMP9021


def solve(available_digits, desired_sum):
    if desired_sum < 0:
        return 0
    if available_digits == 0:
        if desired_sum == 0:
            return 1
        else:
            return 0
    # Either take the last digit d from available_digits and try to get desired_sum - d
    # from the remaining digits, or do not take the last digit and
    # try to get desired_sum from the remaining digits.
    return solve(available_digits // 10, desired_sum) + solve(available_digits // 10, desired_sum - available_digits % 10)
  # for 12234 and 5, it will be solve(1223, 5) + solve(1223, 5 - 4)
  # => solve(1223, 5) + solve(1223, 1)

available_digits = int(input('Input a number that we will use as available digits: '))
desired_sum = int(input('Input a number that represents the desired sum: '))

nb_of_solutions = solve(available_digits, desired_sum)
if nb_of_solutions == 0:
    print('There is no solution.')
elif nb_of_solutions == 1:
    print('There is a unique solution')
else:
    print('There are {:} solutions.'.format(nb_of_solutions))
