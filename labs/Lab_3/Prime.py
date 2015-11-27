for num in range(10000, 99999):
    # prime numbers greater than 1
    if num > 1:
        for i in range(2,num):
            if (num % i) == 0:
                break

        else:
            num += (2**i)
            
rotated_encoded_set = 0
for j in rotated_encoded_list:
    rotated_encoded_set = rotated_encoded_set + (2 ** j)
