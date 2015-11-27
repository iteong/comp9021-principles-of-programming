# Write a program named pascal_triangle.py that prompts the user for a
# nonnegative integer N and displays the first N + 1 rows of Pascal triangle.
#
# Written by Ivan Teong for COMP9021


# Generates the next row of the Pascal Triangle using the length of the
# previous row to return the new row using arithmetic formula to calculate the
# element values within specified range of if-loop followed by last element in
# the row which is row[-1]:

def next_row(row):
    n = len(row)
    new_row = [row[0]] + [row[i] + row[i+1] for i in range(n - 1)] + [row[-1]]
    return new_row

# Uses the previous row to generate the element values of the next row for N+1
# rows, using the next_row function defined earlier, appending the calculated
# values into the list called triangle:

def generate_triangle(row_count):
    row1 = [1]
    triangle = [row1]
    for i in range(1, row_count + 1):
        triangle.append(next_row(triangle[-1]))
    return triangle

# Flag value is False by default. When user input consists of purely digits,
# then convert string input into an integer and if the integer is positive,
# flag value will change to True and user will exit this loop to the next code.
# However, if the user input does not contain purely of digits or the digits
# contain a negative sign ("zero", "-10", "abc10"), then pass returns user to
# input prompt again since flag value is still False.

flag = False
while flag == False:
    rows_input = input('Enter a nonnegative integer: ')
    if rows_input.isdigit() == True:
        rows_input = int(rows_input)
        flag = True
    else:
        pass

# Pascal is all the element values of the triangle generated from the rows_input
# entered by user in list format without the proper formatting:
   
pascal = generate_triangle(rows_input)

# Find the largest_element in the triangle by finding the last row in triangle
# and looking at the middle element which is half of the length of the triangle,
# then calculate the string length of the largest_element:


largest_element = pascal[-1][len(pascal[-1]) // 2]
element_width = len(str(largest_element))
    

# Change each element into the same width as the largest element, justifying
# it to the right with the numerical digits at the end of the element block
# (e.g. a 1-digit number will be put into a block of space+space+number which
# makes up the same string length of the largest element which has a string
# length of 3:

for i in range(0, rows_input+1):
    for j in range(0, i+1):
        pascal[i][j] = str(pascal[i][j]).rjust(element_width)


# Calculate the begin_space in front of each centered element, where each
# element has to shift x - i times where x is the number of rows and i is
# the current row number for the elements, and append spacing ' ' using the
# calculated begin_space into the pascal triangle:

for i in range(0, rows_input+1):
    
    begin_space = (rows_input+1-i) * element_width
    pascal[i].insert(0, ' ' * begin_space)

# Interval is the spacing between the blocks of elements with width of the
# largest element, multiplying ' ' by the element_width:

    interval = ' ' * element_width

# Print the transformed elements that have same width as the largest_element
# and have the begin_space spacing before them, joining them with the interval
# spacing between each element:

    print(interval.join(pascal[i]))
