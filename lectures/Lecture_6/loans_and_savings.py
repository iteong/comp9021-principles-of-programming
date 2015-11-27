# Defines a class Savings and a class Loans that both derive from a class LoanOrSavings,
# keeping up to date all parameters that can be derived from those that have been fixed,
# and allowing one to change the latter.
#
# Written by Eric Martin for COMP9021

from math import log10


INTEREST = 'Interest'
REFERENCE_PERIOD = 'Reference period'
TERM_AMOUNT = 'Term amount'
DURATION = 'Duration'
INITIAL_SUM = 'Initial sum'
FINAL_SUM = 'Final sum'


class LoanOrSavings:
    def __init__(self, of_Savings_type, *, interest = None, reference_period = 'year', term_amount = None, duration = None):
        self._of_savings_type = of_Savings_type
        self._reference_periods = {'year' : 1, 'semester' : 2, 'quarter' : 4, 'month' : 12} 
        self._parameters = {}
        self._unknowns = {INITIAL_SUM, TERM_AMOUNT, FINAL_SUM, DURATION}
        self.set_reference_period(reference_period)
        self.set_interest(interest)
        self.set_term_amount(term_amount)
        self.set_duration(duration)
                
    def set_term_amount(self, term_amount):
        if not term_amount:
            term_amount = 0
        if self._of_savings_type:
            sign = 1
        else:
            sign = -1
        self._check_and_set_parameter(term_amount, TERM_AMOUNT, [int, float], sign)

    def set_reference_period(self, reference_period):
        if reference_period not in self._reference_periods.keys():
            raise ValueError('Reference period should be one of {:}'.format(self._reference_periods.keys))
        self._parameters[REFERENCE_PERIOD] = self._reference_periods[reference_period]
        self.reference_period = reference_period

    def set_interest(self, interest):
        if not interest:
            interest = 0.0
        self._check_type(interest, INTEREST, [int, float])
        if interest == 0:
            raise ValueError('Interest should not be 0')          
        if interest < 0:
            raise ValueError('Interest should not be negative')          
        self._parameters[INTEREST] = interest
        self.effective_interest = (1 + self._parameters[INTEREST] / self._parameters[REFERENCE_PERIOD]) ** self._parameters[REFERENCE_PERIOD] - 1

    def set_duration(self, duration):
        if not duration:
            duration = 0
        self._check_and_set_parameter(duration, DURATION, [int], 1)

    def _check_and_set_parameter(self, parameter, parameter_name, valid_types, sign):
        self._check_type(parameter, parameter_name, valid_types)
        self._set_parameter(parameter, parameter_name, sign)
        
    def _check_type(self, parameter, parameter_name, valid_types):
        if all(not isinstance(parameter, valid_type) for valid_type in valid_types):
            raise TypeError('{:} should be of type in {:}'.format(parameter_name, valid_types))

    def _set_parameter(self, parameter, parameter_name, sign):
        if parameter * sign < 0:
            raise ValueError('{:} should be of opposite sign'.format(parameter_name))
        if parameter == 0:
            parameter = None
        self._parameters[parameter_name] = parameter
        if parameter:
            if parameter_name in self._unknowns:
                if len(self._unknowns) == 1:
                    raise NoUnknownException('{:} is the only unknown parameter'.format(parameter_name))
                self._unknowns.remove(parameter_name)
        else:
            self._unknowns.add(parameter_name)
                                                        
    def update(self):
        all_known = self.solve()
        print('Annual interest:\t {:.2f}%'.format(float(self._parameters[INTEREST] * 100)))
        print('Reference period:\t', self.reference_period)
        if not self._of_savings_type:
            if all_known or INITIAL_SUM not in self._unknowns:
                print('Sum borrowed:\t\t {:.2f}'.format(float(self._parameters[INITIAL_SUM])))
            else:
                print('Sum borrowed:\t\t Unknown')
        if all_known or TERM_AMOUNT not in self._unknowns:
            if self._of_savings_type:
                print('Monthly deposits:\t {:.2f}'.format(float(self._parameters[TERM_AMOUNT])))
            else:
                print('Monthly repayments:\t {:.2f}'.format(float(self._parameters[TERM_AMOUNT])))
        else:
            if self._of_savings_type:
                print('Monthly deposits:\t Unknown')
            else:
                print('Monthly repayments:\t Unknown')
        if self._of_savings_type:
            if all_known or FINAL_SUM not in self._unknowns:       
                print('Available sum:\t\t {:.2f}'.format(float(self._parameters[FINAL_SUM])))
            else:
                print('Available sum:\t\t Unknown')
        if all_known or DURATION not in self._unknowns:
            print('Duration (in years):\t', round(self._parameters[DURATION]))
        else:
            print('Duration (in years):\t Unknown')


class Savings(LoanOrSavings):
    # term_amount is a yearly deposit
    def __init__(self, *, interest = 0, reference_period = 'year', term_amount = 0, duration = 0, final_sum = 0):
        super().__init__(True, interest = interest, reference_period = reference_period, term_amount = term_amount, duration = duration)
        self._unknowns.remove(INITIAL_SUM)
        self._check_type(final_sum, FINAL_SUM, [int, float])
        if len(self._unknowns) == 1 and final_sum > 0:
            raise NoUnknownException('No parameter is unknown')                                            
        self._set_parameter(final_sum, FINAL_SUM, 1)

    def set_final_sum(self, final_sum):
        if not final_sum:
            final_sum = 0
        self._check_and_set_parameter(final_sum, FINAL_SUM, [int, float], 1)

    def solve(self):
        if len(self._unknowns) != 1:
            return False
        if FINAL_SUM in self._unknowns:
            self._parameters[FINAL_SUM] = self._parameters[TERM_AMOUNT] / self.effective_interest * \
                                             ((1 + self.effective_interest) ** (self._parameters[DURATION] + 1) - (1 + self.effective_interest))
        elif TERM_AMOUNT in self._unknowns:
            self._parameters[TERM_AMOUNT] = self._parameters[FINAL_SUM] * self.effective_interest / \
                                         ((1 + self.effective_interest) ** (self._parameters[DURATION] + 1) - (1 + self.effective_interest))
        else:
            self._parameters[DURATION] = log10(self._parameters[FINAL_SUM] * self.effective_interest / self._parameters[TERM_AMOUNT] + \
                                                + (1 + self.effective_interest)) / \
                                                log10(1 + self.effective_interest) - 1
        return True


class Loan(LoanOrSavings):
    # term_amount is a monthly repayment
    def __init__(self, *, interest = 0, reference_period = 'year', term_amount = 0, duration = 0, initial_sum = 0):
        super().__init__(False, interest = interest, reference_period = reference_period, term_amount = term_amount, duration = duration)
        if len(self._unknowns) == 1:
            raise NoUnknownException('No parameter is unknown')                                            
        self.set_initial_sum(initial_sum)
        self._parameters[FINAL_SUM] = 0
        self._unknowns.remove(FINAL_SUM)

    def set_initial_sum(self, initial_sum):
        if not initial_sum:
            initial_sum = 0
        self._check_and_set_parameter(initial_sum, INITIAL_SUM, [int, float], 1)

    def solve(self):
        if len(self._unknowns) != 1:
            return False
        monthly_interest = (1 + self.effective_interest) ** (1 / 12) - 1
        if  INITIAL_SUM in self._unknowns:
            self._parameters[INITIAL_SUM] = -self._parameters[TERM_AMOUNT] * ((1 + monthly_interest) ** (12 * self._parameters[DURATION]) - 1) / \
                                              monthly_interest / (1 + monthly_interest) ** (12 * self._parameters[DURATION])
        elif TERM_AMOUNT in self._unknowns:
            self._parameters[TERM_AMOUNT] = -self._parameters[INITIAL_SUM] * (1 + monthly_interest) ** (12 * self._parameters[DURATION]) * \
                                          monthly_interest / ((1 + monthly_interest) ** (12 * self._parameters[DURATION]) - 1)
        else:
            self._parameters[DURATION] = log10(self._parameters[TERM_AMOUNT] / \
                                                 (monthly_interest * self._parameters[INITIAL_SUM] + self._parameters[TERM_AMOUNT])) / \
                                           (12 * log10(1 + monthly_interest))
        return True

        
class NoUnknownException(Exception):
    pass


if __name__ == '__main__':
    print('TESTING SAVINGS\n')
    savings = Savings(term_amount = 1000, interest = 0.08, duration = 25)
    savings.update()
    print()
    savings.set_term_amount(None)
    savings.update()
    print()
    savings.set_final_sum(78954.42)
    savings.update()
    print()
    savings.set_duration(None)
    savings.update()
    print()
    savings.set_term_amount(1000.00)
    savings.update()
    print('\n\nTESTING LOANS\n')
    loan = Loan(initial_sum = 100000, interest = 0.08, duration = 20, reference_period = 'month')
    loan.update()
    print()
    loan.set_initial_sum(0)
    loan.update()
    print()
    loan.set_term_amount(-836.44)
    loan.update()
    print()
    loan.set_duration(0)
    loan.update()
    print()
    loan.set_initial_sum(100000.0)
    loan.update()
    
        
