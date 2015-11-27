# Prompts the user for a strictly positive number N
# and outputs an equilateral triangle of height N.
# The top of the triangle (line 1) is labeled with the letter A.
# For all nonzero p < N, line p+1 of the triangle is labeled
# with letters that go up in alphabetical order modulo 26
# from the beginning of the line to the middle of the line,
# starting wth the letter that comes next in alphabetical order
# modulo 26 to the letter in the middle of line p,
# and then down in alphabetical order modulo 26
# from the middle of the line to the end of the line.
#
# Written by Eric Martin for COMP9021

while True:
    try:
        height = int(input('Enter strictly positive number: '))
        if height <= 0:
            raise Exception
        break
    except:
        print('Incorrect input, try again.')

A_code = ord('A')
c = A_code

for i in range(1, height + 1):
    # Displays spaces on the left
    for j in range(height - i):
        print(' ', end = '')
    # Displays letters before middle column
    for k in range(1, i):
        print(chr(c), end = '')
        # code of next letter
        c = (c - A_code + 1) % 26 + A_code
    # Displays middle column
    print(chr(c), end = '')
    # Displays letters after middle column
    for k in range(1, i):
        # Code of previous letter
        c = (c - A_code + 25) % 26 + A_code
        print(chr(c), end = '')
    print()
    # Code of first letter to be input on next line
    c = ((1 + i) * i // 2) % 26 + A_code
