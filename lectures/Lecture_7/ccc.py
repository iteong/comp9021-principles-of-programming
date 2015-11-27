def print_numbers_from_to(i, j):
    if i > j:
        return # when it goes beyond the closing range, return means stop
    
    print(i)

    print_numbers_from_to(i+1, j)

    print(i)


# f(2, 5) => 2 ..
# f(3, 5) => 3 ...
# f(4, 5) => 4 ...
# f(5, 5) => 5
# f(6, 5) => 5 (6 > 5, so will reverse to f(5, 5) for values)
# 4
# 3
# 2
