# Write a program named multiplication.py that solves the multiplication in such a way
# that:
#
#                        *  *  *    <==== x
#                    X   *  *  *    <==== y
#                        -------
#                     *  *  *  *    <==== product0
#                  *  *  *  *       <==== product1
#               *  *  *  *          <==== product2
#               ----------------
#               *  *  *  *  *  *    <==== total
#
# - each start stands for a digit, with the leftmost star on each line standing for
# a nonzero digit;
# - all digits on a given line are distinct;
# - the sum of all digits on a given line is the same for the 6 lines.
#
# Written by Ivan Teong for COMP9021

for x in range(100, 1000):
    for y in range(100, 1000):
        
        # x as x1 x2 x3:
        x1 = x // 100;
        x2 = (x // 10) % 10;
        x3 = x % 10;
        # j as j1 j2 j3:
        y1 = y // 100;
        y2 = (y // 10) % 10;
        y3 = y % 10;
        
# Generating different results after multiplication, continue looping if the
# result is less than required number of digits:

        product0 = x * (y % 10)
        if product0 < 1000:
            continue
        else:
        # product0 as p1 p2 p3 p4:
            p1 = product0 // 1000;
            p2 = (product0 // 100) % 10;
            p3 = (product0 // 10) % 10;
            p4 = product0 % 10
            
        product1 = x * ((y // 10) % 10)
        if product1 < 1000:
            continue
        else:
        # product1 as p10 p11 p12 p13:
            p10 = product1 // 1000;
            p11 = (product1 // 100) % 10;
            p12 = (product1 // 10) % 10;
            p13 = product1 % 10
            
        product2 = x * (y // 100)
        if product2 < 1000:
            continue
        else:
        # product2 as p20 p21 p22 p23:
            p20 = product2 // 1000;
            p21 = (product2 // 100) % 10;
            p22 = (product2 // 10) % 10;
            p23 = product2 % 10
            
        total = product0 + (10 * product1) + (100 * product2)
        if total >= 1000000:
            continue
        else:
        # total as t1 t2 t3 t4 t5 t6:
            t1 = total // 100000;
            t2 = (total // 10000) % 10;
            t3 = (total // 1000) % 10;
            t4 = (total // 100) % 10;
            t5 = (total // 10) % 10;
            t6 = total % 10          


# Checking if all digits on a given line are distinct:
        set_x = set([x1, x2, x3])
        if len(set_x) != 3:
            continue

        set_y = set([y1, y2, y3])
        if len(set_y) != 3:
            continue

        set_product0 = set([p1, p2, p3, p4])
        if len(set_product0) != 4:
            continue

        set_product1 = set([p10, p11, p12, p13])
        if len(set_product1) != 4:
            continue

        set_product2 = set([p20, p21, p22, p23])
        if len(set_product2) != 4:
            continue

        set_total = set([t1, t2, t3, t4, t5, t6])
        if len(set_total) != 6:
            continue


# Checking if the sum of all digits in a given line is the same for all 6 lines:

        sum = x1 + x2 + x3
        if  y1 + y2 + y3 != sum:
            continue
        if  p1 + p2 + p3 + p4 != sum:
            continue
        if  p10 + p11 + p12 + p13 != sum:
            continue
        if  p20 + p21 + p22 + p23 != sum:
            continue
        if  t1 + t2 + t3 + t4 + t5 + t6 != sum:
            continue


        print("%6d\n x%4d" % (x,y));
        print("   ---");
        print("%6d\n%5d\n%4d" % (product0, product1, product2));
        print("------");
        print("%d" % (total))
