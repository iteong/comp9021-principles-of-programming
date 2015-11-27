# Decodes all multiplications of the form
#
#                        *  *  *
#                   x       *  *
#                     ----------
#                     *  *  *  *
#                     *  *  *
#                     ----------
#                     *  *  *  *
#
# such that the sum of all digits in all 4 columns is constant.
#
# Written by Eric Martin for COMP9021


for x in range(100, 1000):
    for y in range(10, 100):
        product0 = x * (y % 10)
        if product0 < 1000:
            continue
        product1 = x * (y // 10)
        if product1 >= 1000:
            continue
        total = product0 + 10 * product1
        if total >= 10000:
            continue
        sum = x % 10 + y % 10 + product0 % 10 + total % 10
        if x // 10 % 10 + y // 10 + product0 // 10 % 10 + product1 % 10 + total // 10 % 10 != sum:
            continue
        if x // 100 + product0 // 100 % 10 + product1 // 10 % 10 + total // 100 % 10 != sum:
            continue
        if product0 // 1000 + product1 // 100 + total // 1000 == sum:
            print('{:} * {:} = {:}, all columns adding up to {:}.'.format(x, y, total, sum))
