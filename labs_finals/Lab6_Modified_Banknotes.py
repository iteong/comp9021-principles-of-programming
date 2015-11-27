# Merged questions for banknotes question
print("Input pairs of the form 'value : number'\n"
      "    to indicate that you have 'number' many banknotes of face value 'value'.")
print('Input these pairs one per line, with a blank line to indicate end of input.\n')
face_quantity = []
while True: # if there is any input in line
    line = input()
    if ':' not in line:
        break # if not in right format
    value, quantity = line.split(':') # split line into 2 at : to value, quantity
    face_quantity.append((int(value), int(quantity))) # list pairs inside face_values
    
amount = int(input('Input the desired amount: '))
face_quantity.sort(reverse=True) # efficiency, sort so that largest in front (50,30),(20,30)
nb_of_values = len(face_quantity) # check how many face values inputted by user
print(face_quantity)
# decompose amount into 1,2,3,4 ... amount, where [min qty banknotes, {} = face_value: needed qty]
# 1 = [1, {1:1}], 2 = [1, {2:1}], 3 = [2, {2:1, 1:1}], .... amount
# i.e. desired amount = $17, inputted amt has $20 face value (3), $10 (4), $2 (5), $1 (8)
mini_subs = [[0, {}]] + [[float('inf'), {}] for i in range(amount)] # create arrays with empty up from 0 to 17
for sub_amount in range(1, amount+1):
    for i in range(nb_of_values):
        value = face_quantity[i][0] # value is largest face_value i.e. $20
        if sub_amount < value: # if sub_amount < value, go next (i.e. $1 < $20, continue to value = $10)
            continue
        if sub_amount == value: # if $1 = $1 (jumped from highest face value to matching face value)
            mini_subs[sub_amount] = [1, {value : 1}]
            continue
        if mini_subs[sub_amount - value][0] >= mini_subs[sub_amount][0]: # if mini_subs[$3-$2][0] = 1, mini_subs[$3][0] = inf
            continue
        complement_dic = mini_subs[sub_amount - value][1] # if it is really the minimum, record the dict values
        # value not in dictionary to prevent error, need to have value inside) # what I have(i.e. 1 of $2, need this to make it 2 of $2) < limit of value (1 of $2) => False => skip to $1
        if value not in complement_dic or complement_dic[value] < face_quantity[i][1]: # check if still have any notes left
            if mini_subs[sub_amount - value][0] + 1 < mini_subs[sub_amount][0]: # check if next combination of nb_of_banknotes < (better:less than) previous combination (found)
                mini_subs[sub_amount][0] = mini_subs[sub_amount - value][0] + 1 # this will change the amt of bank notes required
                mini_subs[sub_amount][1].clear() # clear up dictionary for the new solution
            dic = complement_dic.copy() # not to mess up previous sub_amounts in prev dictionary, dic will take the values of the optimal solution (sub_amount-value) + the current value which will add to sub_amount
            if value not in complement_dic:
                dic[value] = 1 # initialising key of dictionary with 1 qty of the value if no key face value
            else:
                dic[value] += 1 # if there is key, increase the key's qty value by 1
            mini_subs[sub_amount][1] = dic
minimal_nb_of_banknote = mini_subs[amount][0] # last one in list and the min nb
if minimal_nb_of_banknote == float('inf'):
    print('There is no solution.')
elif minimal_nb_of_banknote == 1:
    print('The minimal number of banknote required is 1.')
else:
    print('The minimal number of banknotes required is {:}.'.format(minimal_nb_of_banknote))
