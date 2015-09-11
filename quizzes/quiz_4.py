# Uses National Data on the relative frequency of given names in the population
# of U.S. births, stored in a directory "names", in files named "yobxxxx.txt
# with xxxx (the year of birth) ranging from 1880 to 2013.
#
# Prompts the user for a female first name, and finds out the years when this
# name was most popular in terms of ranking. Displays the ranking, and the years
# in decreasing order of frequency.
# 
# Written by Ivan Teong and Eric Martin for COMP9021


import sys
import os

targeted_first_name = input('Enter a female first name: ')
rank = float('inf')

best_years = []

# Create a list, years_list, for female first names, indexing each row as the
# rank using the enumerate function starting from 1 rather than 0, since each
# txt file is already sorted from highest to lowest tally.

years_list = []
item = []
previous_rank = 0

for filename in os.listdir('names'):
    if not filename.endswith('.txt'):
        continue
    file = open('names/' + filename, 'r')
    total = 0
    flag = False
    
    for i, line in enumerate(file, start=1):
        rank = i
        year = ''
        
        for c in filename:
            if c.isdigit():
                year += c
        first_name, sex, tally = line.split(',')

        if sex == 'F':
            total += int(tally)
            
        if targeted_first_name in line:
            if targeted_first_name == first_name:
                if sex == 'M':
                    continue
                else:
# Comparing the rank between the previous and current rank for each given year,
# retaining only the lowest rank that is more than 0. Throw away all elements in
# the years_dict list containing the elements from the previous_rank by emptying
# it, if current rank is less than previous_rank.
                    if previous_rank == 0:
                        previous_rank = rank
                    elif rank < previous_rank:
                        previous_rank = rank
                        years_list = []
                        
                    elif rank > previous_rank:
                        continue
# For all elements that fulfill condition of being the highest rank, append the
# elements in format year/rank/tally into the years_list list which will give
# [[2011, 1, 21799], [2012, 1, 22245], [2013, 1, 21075]] for Sophia. Change the
# flag value to True so that we can do something when this happens.
                    item = [int(year), rank, int(tally)]
                    years_list.append(item)
                    flag = True

# Convert the tally of last year it appears (3rd element in sublist) into
# frequency by dividing it by total, activating when flag is True which is when an
# additional year data is added to the list.
    if flag == True:	
        years_list[-1][2] /= total 
                    
    file.close() 

# Sort the years_list by the frequency which is the 3rd element (or index 2) of
# each sublist, starting from highest to lowest frequency, which is a descending
# order of frequency.
years_list.sort(key=lambda x: x[2], reverse = True)

# Put the years_list into best_years (which is an empty list).
best_years = years_list


if not best_years:
    print('{:} is not a female first name in my records.'.format(targeted_first_name))
else:
    print('By decreasing order of frequency, {:} was most popular in the years: '.format(targeted_first_name), end = '')
    for year in best_years:
# Print only the first element for each item in best_years list
        print(year[0], end = ' ')
        rank = year[1]
    print('\nIts rank was {:} then.'.format(rank))
