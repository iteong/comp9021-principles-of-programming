# Utility to prompt the user for an integer with a range that can be specified,
# until the user input is of the expected type.
#
# Written by Eric Martin for COMP9021

def input_int(prompt = 'What do you want N to be? ', min = float('-inf'), max = float('inf')):
    correct_input = False
    while not correct_input:
        input_string = input(prompt)
        try:
            input_value = int(input_string)
            correct_input = True
        except:
            print('Incorrect input. ', end = '')
        else:
            if input_value < min or input_value > max:
                print('Incorrect input')
                correct_input = False
    return input_value
