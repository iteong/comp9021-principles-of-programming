# Gets as input two strings of digits, sigma and tau,
# and computes natural numbers a and b such that
# a / b is equal to 0.(sigma)(tau)(tau)(tau)(tau)...
# For instance, if sigma is 23 and tau is 905,
# then a could be 23882 and b could be 99900,
# or a could be 11941 and b could be 49950,
# because 23882 / 99900 == 11941 / 49950 == 0.23905905905905905905...
# 11941 / 49950 is in reduced form, but 23882 / 99900 is not.
#
# The fraction a / b is not necessarily reduced,
# but if a is 0 then b is set to 1,
# and if a and b are equal then both are set to 1.
#
# Written by Eric Martin for COMP9021

def get_input(input_name):
    while True:
        text_input = input('Input {}: '.format(input_name))
        try:
            number_input = int(text_input)
            if number_input < 0:
                raise Exception
            return text_input
        except:
            print('Incorrect input, try again.')

print('We want to compute a fraction, say a / b, that evaluates to .(sigma)(tau)(tau)(tau)...')

sigma_input = get_input('sigma')
tau_input = get_input('tau')
sigma = int(sigma_input)
tau = int(tau_input)
# 0.(sigma)(tau)(tau)(tau)... = sigma * 10^{-|sigma)} + tau(10^{-|sigma|-|tau|} +
#                                                           10^{-|sigma|-2|tau|} +
#                                                           10^{-|sigma|-3|tau|} +
#                                                           ...)
#                             = sigma * 10^{-|sigma)} + tau * 10^{-|sigma|-|tau|} / (1 - 10^{-|tau|})
#                             = sigma * 10^{-|sigma)} + tau * 10^{-|sigma|} / (10^{|tau|} - 1)
#                             = [sigma * 10^{-|sigma|} * (10^{|tau|} - 1) + tau * 10^{-|sigma|}] / (10^{|tau|} - 1)
#                             = [sigma * (10^{|tau|} - 1) + tau] / [(10^{|tau|} - 1) * 10^{|sigma|}]    	
numerator = sigma * (10 ** len(tau_input) - 1) + tau
denominator = (10 ** len(tau_input) - 1) * 10 ** len(sigma_input)
if numerator == 0:
    denominator = 1
# In case sigma and tau consist of nothing but 9s
if numerator == denominator:
    numerator = denominator = 1
		
print('The fraction is: {} / {}'.format(numerator, denominator))
print('It evaluates to: {}'.format(numerator / denominator))

