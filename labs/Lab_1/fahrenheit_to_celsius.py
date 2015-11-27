# Prints out a conversion table of temperatures from Fahrenheit
# to Celsius degrees, with the former ranging from 0 to 300 in steps of 20.
#
# Written by Eric Martin for COMP9021

min_temperature = 0
max_temperature = 300
step = 20

print('Fahrenheit\tCelsius')
for fahrenheit in range(min_temperature, max_temperature + step, step):
    celsius = 5 * (fahrenheit - 32) / 9
    print('{:10d}\t{:7.1f}'.format(fahrenheit, celsius)) # 10d:  A decimal number in a field of width 10,
                                                         # \t:   A tab
                                                         # 7.1f: A floating point number in a field of width 7
                                                         #       with 1 digit after the decimal point
    
    
