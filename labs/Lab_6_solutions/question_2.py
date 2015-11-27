# Prompts the user for the face values of banknotes and their associated quantities
# as well as for an amount, and if possible, outputs the minimal number of banknotes
# needed to match that amount, as well as the detail of how many banknotes of each type value are used.
#
# Written by Eric Martin for COMP9021


def print_solution(solution):
    max_width = max([len(str(value)) for value in solution]) + 1
    for value in sorted(solution.keys()):
        print('{:>{:}}: {:}'.format('$' + str(value), max_width, solution[value]))

            
print("Input pairs of the form 'value : number'\n"
      "   to indicate that you have 'number' many banknotes of face value 'value'.")
print('Input these pairs one per line, with a blank line to indicate end of input.\n')
face_values = []
while True:
    line = input()
    if ':' not in line:
        break
    value, quantity = line.split(':')
    face_values.append((int(value), int(quantity)))
# Might make the computation more efficient.
face_values.sort(reverse = True)
nb_of_face_values = len(face_values)
amount = int(input('Input the desired amount: '))

# minimal_combinations[sub_amount] will be a pair whose first element is the minimal number of banknotes
# needed to yield sub_amount, and whose second element is the list of all possible solutions,
# each solution being a dictionary with face values as keys and number of banknotes used as values.
minimal_combinations = [[0, []]] + [[float('inf'), []] for i in range(amount)]
for sub_amount in range(1, amount + 1):
    for i in range(nb_of_face_values):
        value = face_values[i][0]
        if sub_amount < value:
            continue
        if value == sub_amount:
            minimal_combinations[sub_amount] = [1, [{value : 1}]]
            continue
        # Using "value" to get "sub_amount" would require most banknotes that the minimum
        # number of banknotes so far found out to sum up to "sub_amount".
        if minimal_combinations[sub_amount - value][0] >= minimal_combinations[sub_amount][0]:
            continue
        for option in minimal_combinations[sub_amount - value][1]:
            # A banknote with face value "value" is available to complete "option" and result in a sum of "sub_amount".
            if value not in option or option[value] < face_values[i][1]:
                # Moreover, it determines a new minimum to then umber of banknotes that can sum of to "sub_amount".
                if minimal_combinations[sub_amount - value][0] + 1 < minimal_combinations[sub_amount][0]:
                    minimal_combinations[sub_amount][0] = minimal_combinations[sub_amount - value][0] + 1
                    minimal_combinations[sub_amount][1].clear()
                extended_option = dict(option)
                if value not in option:
                    extended_option[value] = 1
                else:
                    extended_option[value] += 1
                if extended_option not in minimal_combinations[sub_amount][1]:
                    minimal_combinations[sub_amount][1].append(extended_option)
minimal_nb_of_banknotes = minimal_combinations[amount][0]
if minimal_nb_of_banknotes == float('inf'):
    print('\nThere is no solution.')
else:
    solutions = minimal_combinations[amount][1]
    nb_of_solutions = len(solutions)
    if nb_of_solutions == 1:
        print('\nThere is a unique solution:')
        print_solution(solutions[0])
    else:
        print('\nThere are {:} solutions:'.format(nb_of_solutions))
        for i in range(nb_of_solutions - 1):
            print_solution(solutions[i])
            print()
        print_solution(solutions[nb_of_solutions - 1])
        

