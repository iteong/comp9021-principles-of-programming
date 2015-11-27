
from math import sqrt, ceil
from random import randint

height = int(input('Please enter height of building: '))
max_nb_of_drops = ceil((-1 + sqrt(1 + 8 * height)) / 2)
print('I need at most {:} drops'.format(max_nb_of_drops))

breaking_floor = randint(1, height + 1)
low = 0
high = height + 1
d = max_nb_of_drops
while low < high - 1:
    level_tested = min(low + d, height)
    if level_tested < breaking_floor:
        print('Marble does not break on level {:}'.format(level_tested))
        low = level_tested
        if d > 1:
            d -= 1
    else:
        print('Marble breaks on level {:}'.format(level_tested))
        high = level_tested
        d = 1
