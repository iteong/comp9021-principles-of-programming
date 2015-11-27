# Determines from National Data on the relative frequency of given names in the population of U.S. births
# the top 10 names that have disappeared and reappeared for the longest period of time.
# The data are stored in a directory "names", in files named "yobxxxx.txt with xxxx (the year of birth)
# ranging from 1880 to2013.
#
# Written by Eric Martin for COMP9021


import sys
import os


# A dictionnary where a key is a name and a value is the list of all years_per_first_name when the name was given.
years_per_first_name = {}
directory = 'names'
for filename in os.listdir(directory):
    if not filename.endswith('.txt'):
        continue
    year = ''
    for c in filename:
        if c.isdigit():
            year += c
    year = int(year)
    file = open(directory + '/' + filename, 'r')
    for line in file:
        first_name = line.split(',')[0]
        if first_name not in years_per_first_name:
            years_per_first_name[first_name] = [year]
        else:
            years_per_first_name[first_name].append(year)
    file.close()

# A list of triples of the form (difference between years_per_first_name when a name was last given and first given again,
#                                year when name was last given,
#                                name).
revivals = []
for first_name in years_per_first_name:
    nb_of_years_per_first_name_in_usage = len(years_per_first_name[first_name])
    if nb_of_years_per_first_name_in_usage == 1:
        continue
    for i in range(nb_of_years_per_first_name_in_usage - 1):
        revivals.append((years_per_first_name[first_name][i + 1] - years_per_first_name[first_name][i], years_per_first_name[first_name][i], first_name))       
revivals = sorted(revivals, reverse = True)

for i in range(10):
    print('{:} was last used in {:} and then again in {:}, {:} years later.'.
          format(revivals[i][2], revivals[i][1], revivals[i][1] + revivals[i][0], revivals[i][0]))
