# Prompts the user for an amount, and outputs the minimal number of banknotes needed to match that amount,
# as well as the detail of how many banknotes of each type value are used.
# The available banknotes have a face value which is one of $1, $2, $5, $10, $20, $50, and $100.
#
# Written by Eric Martin for COMP9021

face_values = [1, 2, 5, 10, 20, 50, 100]
amount = int(input('Input the desired amount: '))

banknotes = []
amount_left = amount
while amount_left:
    value = face_values.pop()
    if amount_left >= value:
        banknotes.append((value, amount_left // value))
        amount_left %= value
nb_of_banknotes = sum(banknote[1] for banknote in banknotes)
if nb_of_banknotes == 1:
    print('\n1 banknote is needed.')
else:
    print('\n{:} banknotes are needed'.format(nb_of_banknotes))
print('The detail is:')
for banknote in banknotes:
    print('{:>4}: {:}'.format('$' + str(banknote[0]), banknote[1]))
    
