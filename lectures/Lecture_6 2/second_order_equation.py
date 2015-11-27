# Represents a second-order equation as a class with
# a, b, c, root_1 and root_2 as data.
# By default, a is set to 1 and b and c are set to 0.
# The parameters can be changed with the update_parameters() function.
# Whether the parameters are changed when the equation is created
# or by a call to the update_parameters() function,
# a, b and c have to be explictly named.
# The roots are automatically computed when the the equation is created
# or when some parameter is updated.
#
# Written by Eric Martin for COMP9021

from math import sqrt

class second_order_equation:
    '''
    >>> eq = second_order_equation()
    >>> eq.a
    1
    >>> eq.b
    0
    >>> eq.c
    0
    >>> eq.root_1
    0.0
    >>> eq.root_2
    0.0
    >>> eq = second_order_equation(b = 4)
    >>> eq.root_1
    -4.0
    >>> eq.root_2
    0.0
    >>> eq = second_order_equation(a = 1, b = 3, c = 2)
    >>> eq.root_1
    -2.0
    >>> eq.root_2
    -1.0
    >>> eq.update_parameters(b = -1)
    >>> eq.root_1
    >>> eq.root_2
    >>> eq.update_parameters(c = 0.3, a = 0.5)
    >>> eq.root_1
    0.3675444679663241
    >>> eq.root_2
    1.632455532033676
    '''
    def __init__(self, *, a = 1, b = 0, c = 0):
        if a == 0:
            print('a cannot be equal to 0.')
            return
        self.a = a
        self.b = b
        self.c = c
        self._compute_delta()
        self._compute_roots()

    def _compute_delta(self):
        self.delta = self.b * self.b - 4 * self.a * self.c

    def _compute_roots(self):
        if self.delta < 0:
            self.root_1 = self.root_2 = None
        elif self.delta == 0:
            self.root_1 = self.root_2 = -self.b / (2 * self.a)
        else:
            sqrt_delta = sqrt(self.delta)
            self.root_1 = (-self.b - sqrt_delta) / (2 * self.a)
            self.root_2 = (-self.b + sqrt_delta) / (2 * self.a)

    def update_parameters(self, *, a = None, b = None, c = None):
        if a == 0:
            print('a cannot be equal to 0.')
            return
        if a != None:
            self.a = a
        if b != None:
            self.b = b
        if c != None:
            self.c = c
        self._compute_delta()
        self._compute_roots()


        


        
