# Prints out a conversion table of temperatures from Celsius
# to Fahrenheit degrees, with the former ranging from 0 to 100 in steps of 10.
#
# Written by Ivan Teong for COMP9021

min_temperature = 0
max_temperature = 100
step = 10

print('Celsius\tFahrenheit')
for celsius in range(min_temperature, max_temperature + step, step):
    fahrenheit = 32 + (celsius*9)/5
    print('{:10d}\t{:7.1f}'.format(celsius, fahrenheit)) # 10d:  A decimal number in a field of width 10,
                                                         # \t:   A tab
                                                         # 7.1f: A floating point number in a field of width 7
                                                         #       with 1 digit after the decimal point
    
    

