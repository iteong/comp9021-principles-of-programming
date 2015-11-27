#import sys as you using:
sys.exit()

if file.endswith('.pdf'):
    continue looking for txt file

file = open('names/' + filename, 'r')
# open the file that is txt extension in names directory, for 'r' reading purpose

open(male_subdirectory + '/' + filename + 'w')
# open the subdirectory/filename and this 'w' is for writing purposes

# from names directory's text file, check each tuple whether it is F or M, copy it and put it
# into names_classified folder and then into the male or female, with just the name
# and year and not the gender, check each entity at the commar ',':
    for line in file:
        (first_name, sex, count) = line.split(',')

        if sex == 'M':
            print(first_name, count, sep = ',', end = '', file = male_file)
            # copy the first name and count into the folder male, change separator
            # to ',', end = '' prints out new line so that it will appear as
            # Janice, 1986 with new line for new entry, and not Jane1985John2000

            male_file.close
            # close folders

# use names as keys

years = {} # dictionary

if first_name not in years:
    # if the person's first name in dictionary is not inside the dictionary, add it:
    years[first_name]

year = '' # start from empty string
for c in filename:
    if c.isdigit(): # if c is a digit, add the name c to my year
        year += c
        #now can assign this new year, but make sure that the value is with only
        #1 element and make it for sure an integer
        years[first_name] = [int(year)]

        years[first_name].append(int(year)) # append the integer year into first name year

        file.close()
        # exit this loop by closing the file

 #       James key, and also the list of years where the name has been used
 #       we want to compute a new dictionary where we store 

# first name, gap and then first year,
# put the oldest date first, then the name, then first year last.

differences = []
# for first_name in years: (dictionary is years)
