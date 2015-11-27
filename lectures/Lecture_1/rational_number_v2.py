# Gets as input two strings of digits, sigma and tau,
# and computes natural numbers a and b such that
# a / b is equal to 0.(sigma)(tau)(tau)(tau)(tau)...
# For instance, if sigma is 23 and tau is 905,
# then a could be 23882 and b could be 99900,
# or a could be 11941 and b could be 49950,
# because 23882 / 99900 == 11941 / 49950 == 0.23905905905905905905...
# 11941 / 49950 is in reduced form, but 23882 / 99900 is not.
#
# Provides two functions:
# - one where the fraction a / b is not necessarily reduced;
# - one where the fraction a / b is reduced
# (which is tractable only if a is small enough).
# In any case, if a is 0 then b is set to 1,
# and if a and b are equal then both are set to 1.
#
# Written by Eric Martin for COMP9021

def determine_fraction():
    output_result(*compute_fraction(*get_both_inputs()))
                    
def determine_reduced_fraction():
    output_result(*reduce_fraction(*compute_fraction(*get_both_inputs())))
    
def get_both_inputs():
    print('We want to compute a fraction, say a / b, that evaluates to .(sigma)(tau)(tau)(tau)...')
    return get_input('sigma'), get_input('tau')

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

def compute_fraction(sigma_input, tau_input):
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
    return numerator, denominator

def reduce_fraction(numerator, denominator):
    possible_factor = 2
    while possible_factor <= numerator // 2:
        while numerator % possible_factor == 0 and denominator % possible_factor == 0:
                numerator //= possible_factor
                denominator //= possible_factor
        possible_factor += 1
    return numerator, denominator

def output_result(numerator, denominator):
    print('The fraction is: {} / {}'.format(numerator, denominator))
    print('It evaluates to: {}'.format(numerator / denominator))

if __name__ == '__main__':
    inputs_to_test = [('0', '0'), ('0', '1'), ('1', '0'), ('1', '1'), ('9', '9'), ('23', '905'),
                      ('1', '234'), ('234', '1'), ('000', '97'), ('97', '000'), ('01234', '543210')]               
    print('NONREDUCED FRACTIONS')
    for sigma, tau in inputs_to_test:
        print('    Testing sigma == {} and tau == {}'.format(sigma, tau))
        output_result(*compute_fraction(sigma, tau))
    print('')
    print('REDUCED FRACTIONS')
    for sigma, tau in inputs_to_test:
        print('    Testing sigma == {} and tau == {}'.format(sigma, tau))
        output_result(*reduce_fraction(*compute_fraction(sigma, tau)))
