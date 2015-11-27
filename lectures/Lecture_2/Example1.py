def reduce(a,b):
    if b % a == 0:
        print(1, b // a)
        return
    factor=2
    while factor <= a // 2:
        while a % factor == 0 and b % factor == 0:
            a //= factor
            b //= factor
            factor += 1
            print(a,b)
            
            
