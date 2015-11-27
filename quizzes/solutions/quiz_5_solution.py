# Defines two classes, Point() and NonVerticalLine().
# An object for the second class is created by passing named arguments,
# point_1 and point_2, to its constructor.
# Such an object can be modified by changing one point or both points thanks to the
# function change_point_or_points().
# At any stage, the object maintains correct values for slope and intersect.
#
# Written by Eric Martin for COMP9021

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
        self._update(p_1 = p1, p_2 = p2)
        return True

    def _change_point_or_points(self, p1, p2):
        if not p1 and not p2:
            return True
        if p1 and p2:
            if p1.x == p2.x:
                return False
            self._update(p1, p2)
            return True
        if p1:
            if p1.x == self.point_2.x:
                return False
            self._update(p_1 = p1)
            return True
        if p2:
            if p2.x == self.point_1.x:
                return False
            self._update(p_2 = p2)
            return True

    def _update(self, p_1 = None, p_2 = None):
        if p_1:
            self.point_1 = p_1
        if p_2:
            self.point_2 = p_2
        self.slope = (self.point_2.y - self.point_1.y) / (self.point_2.x - self.point_1.x)
        self.intercept = self.point_1.y - self.slope * self.point_1.x
        
        
