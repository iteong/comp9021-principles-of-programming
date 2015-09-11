# Defines two classes, Point() and NonVerticalLine().
# An object for the second class is created by passing named arguments,
# point_1 and point_2, to its constructor.
# Such an object can be modified by changing one point or both points thanks to the
# function change_point_or_points().
# At any stage, the object maintains correct values for slope and intersect.
#
# Written by Ivan Teong and Eric Martin for COMP9021

class Point():
    def __init__(self, x = None, y = None):
        if x == None and y == None:
            self.x = 0
            self.y = 0
        elif x == None or y == None:
            print('Need two coordinates, point not created.')
        else:
            self.x = x
            self.y = y
    
class NonVerticalLine:
    def __init__(self, *, point_1, point_2):
        if not self._check_and_initialise(point_1, point_2):
            print('Incorrect input, line not created.')
            return

    def change_point_or_points(self, *, point_1 = None, point_2 = None):
        if not self._change_point_or_points(point_1, point_2):
            print('Could not perform this change.')
            return

    def _check_and_initialise(self, p1, p2):
        if p1.x == p2.x:
            return False
        else:
            # need to keep a record of p1 and p2, just like how Point() keeps
            # the values of x and y, if you don't do these, then you can't keep
            # track of p1 and p2.
            self.p1 = p1
            self.p2 = p2
            if p1.y > p2.y:
                self.slope = (p1.y - p2.y)/(p1.x - p2.x)
                self.intercept = p1.y - self.slope * p1.x
            else:
                self.slope = (p2.y - p1.y)/(p2.x - p1.x)
                self.intercept = p2.y - self.slope * p2.x
            return True
        
        # this function should return false if the line is vertical
        # otherwise it should return true

    def _change_point_or_points(self, a, b):
    # check if the argument for this function is empty, will not output if not
        if a == None and b == None:
            return True
    # check if you did not input any change for either point, just one input
        elif a == None:
            a = self.p1
        elif b == None:
            b = self.p2
    # check if arguments entered will output a vertical line
        if a.x == b.x:
            return False
        else:
            # do conversion if it is legal input, calling a private function
            # (encapsulation), which can be only called within the class, Python
            # does not prohibit you to call private functions outside the class,
            # unlike C++, but it is not good coding practice.
            self._check_and_initialise(a, b)
            return True
    
    # Possibly define other functions

'''
class Phone():
    def __init__(self, number):
        self. number = number
    def change_number(self, new_number):
        self.number = new_number

ivans_phone = Phone(0412345678)

ivans_phone.change_number(0487654321)
'''
