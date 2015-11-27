# Uses National Data on the relative frequency of given names in the population of U.S. births,
# stored in a directory "names", in files named "yobxxxx.txt with xxxx (the year of birth)
# ranging from 1880 to2013.
# Prompts the user for a female first name, and finds out the years when this name was most popular
# in terms of ranking. Displays the ranking, and the years in decreasing order of frequency.
# 
# Written by Eric Martin for COMP9021


import sys
import os

targeted_first_name = input('Enter a female first name: ')
rank = float('inf')

best_years = []
frequencies = []
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
    line_nb = 1
    tally = 0
    improved_ranking = False
    equalised_ranking = False
    for line in file:
        first_name, sex, count = line.split(',')
        if sex == 'M':
            break
        count = int(count)
        tally += count
        if first_name == targeted_first_name:
            if line_nb < rank:
                best_years = [year]
                rank = line_nb
                recorded_count = count
                improved_ranking = True
            elif line_nb == rank:
                best_years.append(year)
                recorded_count = count
                equalised_ranking = True
        line_nb += 1
    if improved_ranking:
        frequencies = [recorded_count / tally]
    elif equalised_ranking:
        frequencies.append(recorded_count / tally)
    file.close()
if best_years:
    frequencies, best_years = tuple(zip(*sorted(zip(frequencies, best_years), reverse = True)))


if not best_years:
    print('{:} is not a female first name in my records.'.format(targeted_first_name))
else:
    print('By decreasing order of frequency, {:} was most popular in the years: '.format(targeted_first_name), end = '')
    for year in best_years:
        print(year, end = ' ')
    print('\nIts rank was {:} then.'.format(rank))
