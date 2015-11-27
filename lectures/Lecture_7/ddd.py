def my_sum_1(i, j):
    result = 0
    for k in range(i, j + 1):
        result += k
    return result

def my_sum_2(i, j):   # ignore first element, and shrink the interval
    if i > j:         # [X [X X X X]]
        return 0      # sum of numbers in empty interval is 0
    return i + my_sum_2(i +1, j)

def my_sum_3(i, j):   # ignore last element, i on right, shrink interval
    if i > j:         # [[X X X X X] X]
        return 0
    return my_sum_3(i, j - 1) + j

def my_sum_4(i, j):   # having 2 intervals added within main interval, add both
    if i > j:         # [[X X X][X X X]] 
        return 0 # if interval is empty, return 0
    if i == j:
        return i
    return my_sum_4(i, (i+j)//2) + my_sum_4((i+j)//2 + 1, j)
    
print(my_sum_1(2, 7))
print(my_sum_2(2, 7))
print(my_sum_3(2, 7))
print(my_sum_4(2, 7))

# adding up all numbers in interval
