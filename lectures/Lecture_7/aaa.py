def fact_1(N):
    result = 1
    for i in range(2, N+1):
        result *= i
    return result

def fact_2(N):
    if N == 0:
        return 1 ## take care of base case (0! = 1)
    return fact_2(N-1) * N

print(fact_1(6))     
print(fact_2(6))
