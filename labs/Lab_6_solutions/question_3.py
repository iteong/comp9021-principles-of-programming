# A class to create fractions and work precisely with them.
#
# Written by Eric Martin for COMP9021

class Fraction():
    def __init__(self, *args):
        try:
            if len(args) != 2:
                raise TypeError
            if not self._validate(*args):
                raise ValueError
        except TypeError:
            print('Provide exactly two arguments.')
        except ValueError:
            print('Provide an integer and a nonzero integer as arguments.')
        else:
            self._set_to_normal_form(*args)
    
    def _validate(self, numerator, denominator):
        if type(numerator) is not int:
            return False
        if type(denominator) is not int:
            return False
        if denominator == 0:
            return False
        return True

    def _set_to_normal_form(self, numerator, denominator):
        if numerator * denominator < 0:
            sign = -1
        else:
            sign = 1
        numerator = abs(numerator)
        denominator = abs(denominator)
        gcd = self._gcd(numerator, denominator)
        self.numerator = sign * numerator // gcd
        self.denominator = denominator // gcd

    def _gcd(self, a, b):
        if b == 0:
            return a
        return self._gcd(b, a % b)

    def __repr__(self):
        return 'Fraction(numerator = {:}, denominator = {:})'.format(self.numerator, self.denominator)

    def __str__(self):
        return '{:} / {:}'.format(self.numerator, self.denominator)
        
    def __add__(self, fraction):
        return Fraction(self.numerator * fraction.denominator + self.denominator * fraction.numerator,
                        self.denominator * fraction.denominator)

    def __sub__(self, fraction):
        return Fraction(self.numerator * fraction.denominator - self.denominator * fraction.numerator,
                        self.denominator * fraction.denominator)

    def __mul__(self, fraction):
        return Fraction(self.numerator * fraction.numerator,  self.denominator * fraction.denominator)

    def __truediv__(self, fraction):
        try:
            if fraction.numerator == 0:
                raise ValueError
        except ValueError:
            print('Cannot divide by 0.')
        else:
            return Fraction(self.numerator * fraction.denominator,  self.denominator * fraction.numerator)

    def __lt__(self, fraction):
        return self.numerator * fraction.denominator < self.denominator * fraction.numerator

    def __le__(self, fraction):
        return self.numerator * fraction.denominator <= self.denominator * fraction.numerator

    def __gt__(self, fraction):
        return self.numerator * fraction.denominator > self.denominator * fraction.numerator

    def __ge__(self, fraction):
        return self.numerator * fraction.denominator >= self.denominator * fraction.numerator

    def __eq__(self, fraction):
        return self.numerator * fraction.denominator == self.denominator * fraction.numerator

    def __ne__(self, fraction):
        return self.numerator * fraction.denominator != self.denominator * fraction.numerator

    
