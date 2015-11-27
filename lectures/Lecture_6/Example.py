# y = ax**2 + bx**2 + c

from math import sqrt

class second_order_equation:
    def __init__(self):
        self.a = 1
        self.b = 0
        self.c = 0
##        self.delta = None
##        self.root_1 = None
##        self.root_2 = None
        self.compute_delta()
        self.compute_roots()

    def compute_delta(self):
    # global delta any variable within functions are local, outside is global
    # if want to refer to global variable, need to say global delta
        self.delta = self.b * self.b - 4 * self.a * self.c

    def compute_roots(self):
##    global root_1
##    global root_2
##    global delta
##    global a
##    global b
##    global c
        if self.delta < 0:
            self.root_1 = None
            self.root_2 = None
        elif self.delta == 0:
            self.root_1 = -self.b / 2 * self.a
            self.root_2 = None
        else:
            sqrt_delta = sqrt(self.delta)
            self.root_1 = (-self.b - sqrt_delta) / (2 * self.a)
            self.root_2 = (-self.b + sqrt_delta) / (2 * self.a)

##a = 1
##change_parameters(0, 1, a = a, b = 2, c = 7) # first a is the argument, second a is the value of a which is 1

    def change_parameters(self, *, a = None, b = None, c = None): # * forces arguments to be keyed where a = 2
##    global a
##    global b
##    global c
        if a:
            self.a = a
        if b != None:
            self.b = b
        if c != None:
            self.c = c
        self.compute_delta()
        self.compute_roots()
        
