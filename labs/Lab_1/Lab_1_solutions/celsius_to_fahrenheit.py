# Prints out a conversion table of temperatures from Celsius to Fahrenheit degrees,
# the former ranging from 0 to 100 in steps of 10.
#
# Written by Eric Martin for COMP9021

min_temperature = 0
max_temperature = 100
step = 10

print('Celsius\tFahrenheit')
for celsius in range(min_temperature, max_temperature + step, step):
    fahrenheit = celsius / 5 * 9 + 32
    print('{:7d}\t{:10.0f}'.format(celsius, fahrenheit))
