def get_input(input_name):
    while True:
        word_input = input('Please enter {:}: '.format(input_name))
        try:
            value_input = int(word_input)
            if value_input < 0:
                raise Exception
            break
        except:
            print('Input is incorrect, try again')
        return len(word_input), value_input

sigma_string, sigma = get_input('sigma')
tau_string, tau = get_input('tau')

a = sigma * (10 ** tau_length - 1) + tau
b =(10 ** tau_length - 1) * 10 ** sigma_length
if a == 0:
    b = 1
if a == b:
    a = b = 1
print('{:} / {:}'.format(a, b))
print(a / b)

