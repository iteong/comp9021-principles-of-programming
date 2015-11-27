# Defines Monomial and Polynomial classes.
# A polynomial is built from a string that represents a polynomial,
# that is, a sum or difference of monomials.
# - The leading monomial can be either an integer,
#   or an integer followed by x,
#   or an integer followed by x\^ followed by a nonnegative integer.
# - The other monomials can be either a nonnegative integer,
#   or an integer followed by x,
#   or an integer followed by x\^ followed by a nonnegative integer.
# Spaces can be inserted anywhere in the string.
#
# Written by Eric Martin for COMP9021


class Monomial:
    def __init__(self, coefficient = 0, degree = 0):
        self.coefficient = coefficient
        self.degree = degree
        self.next_monomial = None


class Polynomial:
    def __init__(self, input_polynomial = None):
        if not input_polynomial:
            self.head = None
            return
        input_polynomial = input_polynomial.replace(' ', '')
        if not input_polynomial:
            self.head = None
            return
        if input_polynomial[0] == '+':
            print('Incorrect input')
            return
        if input_polynomial[0] == '-' and len(input_polynomial) > 1 and input_polynomial[1] == '0':
            print('Incorrect input')
            return            
        for i in range(1, len(input_polynomial)):
            if input_polynomial[i] in '+-' and not input_polynomial[i - 1].isdigit() and input_polynomial[i - 1] != 'x':
                print('Incorrect input')
                return
        input_polynomial = input_polynomial.replace('-', '+-').split('+')
        # For the case where the leading factor is negative.
        if not input_polynomial[0]:
            input_polynomial = input_polynomial[1: ]
        monomial = self._get_monomial(input_polynomial[0])
        if not monomial:
            print('Incorrect input')
            return
        self.head = monomial
        for input_monomial in input_polynomial[1: ]:
            monomial = self._get_monomial(input_monomial)
            if not monomial:
                print('Incorrect input')
                return
            if not monomial.coefficient:
                continue
            self._add_monomial(monomial)

    def _copy(self):
        copy = Polynomial()
        if not self.head:
            return copy
        copy.head = Monomial(self.head.coefficient, self.head.degree)
        node = self.head.next_monomial
        node_copy = copy.head
        while node:
            node_copy.next_monomial = Monomial(node.coefficient, node.degree)
            node = node.next_monomial
            node_copy = node_copy.next_monomial
        return copy
            
    def _get_monomial(self, input_monomial):
        monomial_parts = input_monomial.split('x')
        if len(monomial_parts) > 2:
            return False
        if len(monomial_parts) == 1:
            try:
                coefficient = int(monomial_parts[0])
                return Monomial(coefficient, 0)
            except:
                return False
        # The case of 'x'.
        if not monomial_parts[0] and not monomial_parts[1]:
            return Monomial(1, 1)
        if not monomial_parts[0]:
            coefficient = 1
        elif monomial_parts[0] == '-':
            coefficient = -1
        else:
            try:
                coefficient = int(monomial_parts[0])
            except:
                return False
        # Needed for the leading monomial.
        if coefficient == 0:
            degree = 0
        else:
            if not monomial_parts[1]:
                degree = 1
            else:
                if monomial_parts[1][0] != '^':
                    return False
                try:
                    degree = int(monomial_parts[1][1: ])
                    if degree < 0:
                        return False
                except:
                    return False           
        return Monomial(coefficient, degree)

    def _add_monomial(self, monomial):
        if not self.head:
            self.head = monomial
            return
        if monomial.degree > self.head.degree:
            monomial.next_monomial = self.head
            self.head = monomial
            return
        if monomial.degree == self.head.degree:
            self._add_monomial_of_same_degree(None, self.head, monomial)
            return              
        node = self.head
        while node.next_monomial and monomial.degree < node.next_monomial.degree:
            node = node.next_monomial
        if not node.next_monomial:
            node.next_monomial = monomial
        elif monomial.degree == node.next_monomial.degree:
            self._add_monomial_of_same_degree(node, node.next_monomial, monomial)
        else:
            monomial.next_monomial = node.next_monomial
            node.next_monomial = monomial
        
    def _add_monomial_of_same_degree(self, parent, node, monomial):
        if node.coefficient + monomial.coefficient:
            node.coefficient += monomial.coefficient
        elif not parent:
            if not self.head.next_monomial:
                self.head = Monomial()
            else:
                self.head = self.head.next_monomial
        else:
            parent.next_monomial = parent.next_monomial.next_monomial

    def _multiply_monomial(self, monomial):
        if not monomial.coefficient:
            self.head.coefficient = 0
            self.head.degree = 1
            self.head.next_monomial = None
            return
        node = self.head
        while node:
            node.coefficient *= monomial.coefficient
            node.degree += monomial.degree
            node = node.next_monomial
         
    def __str__(self):
        if not self.head:
            return ''
        if not self.head.degree:
            return str(self.head.coefficient)
        if self.head.coefficient == 1:
            output = ''
        elif self.head.coefficient == -1:
            output = '-'
        else:
            output = str(self.head.coefficient)
        output += 'x'
        if self.head.degree > 1:
            output += '^'
            output += str(self.head.degree)
        node = self.head
        while node.next_monomial:
            node = node.next_monomial
            if node.coefficient > 0:
                output += ' + '
            else:
                 output += ' - '
            if abs(node.coefficient) != 1 or node.degree == 0:
                output += str(abs(node.coefficient))
            if node.degree:
                output += 'x'
            if node.degree > 1:               
                output += '^'
                output += str(node.degree)
        return output
                   
    def __add__(self, polynomial):
        copy = self._copy()
        node = polynomial.head
        while node:
            copy._add_monomial(Monomial(node.coefficient, node.degree))
            node = node.next_monomial
        return copy

    def __mul__(self, polynomial):
        product = Polynomial()
        node = polynomial.head
        while node:
            product_by_monomial = self._copy()
            product_by_monomial._multiply_monomial(Monomial(node.coefficient, node.degree))
            second_node = product_by_monomial.head
            while second_node:
                product._add_monomial(Monomial(second_node.coefficient, second_node.degree))
                second_node = second_node.next_monomial
            node = node.next_monomial
        return product

    def __sub__(self, polynomial):
        return self.__add__(polynomial.__mul__(Polynomial('-1')))

    def __truediv__(self, polynomial):
        quotient = Polynomial()
        copy = self._copy()
        while copy.head.coefficient and copy.head.degree:
            if copy.head.coefficient % polynomial.head.coefficient:
                return None
            if copy.head.degree < polynomial.head.degree:
                return None
            polynomial_copy = polynomial._copy()
            coefficient = copy.head.coefficient // polynomial.head.coefficient
            degree = copy.head.degree - polynomial.head.degree
            polynomial_copy._multiply_monomial(Monomial(-coefficient, degree))
            copy = copy.__add__(polynomial_copy)
            quotient._add_monomial(Monomial(coefficient, degree))                                     
        return quotient

if __name__ == '__main__':
   Polynomial('-0')
   Polynomial('+0')
   Polynomial('0x^-1')
   Polynomial('2x + +2')
   Polynomial('2x + -2')
   Polynomial('2x - +2')
   poly_0 = Polynomial('0')
   print(poly_0)
   poly_0 = Polynomial('0x')
   print(poly_0)
   poly_0 = Polynomial('0x^0')
   print(poly_0)
   poly_0 = Polynomial('0x^5')
   print(poly_0)
   poly_1 = Polynomial('x')
   print(poly_1)
   poly_1 = Polynomial('1x')
   print(poly_1)
   poly_1 = Polynomial('1x^1')
   print(poly_1)
   poly_2 = Polynomial('2')
   print(poly_2)
   poly_2 = Polynomial('2x^0')
   print(poly_2)
   poly_3 = Polynomial('1 + 2-3 +10')
   print(poly_3)
   poly_4 = Polynomial('x + x - 2x -3x^1 + 3x')
   print(poly_4)
   poly_5 = Polynomial('x + 2 + x - x -3x^1 + 3x + 5x^0')
   print(poly_5)
   poly_6 = Polynomial('-2x + 7x^3 +x   - 0  + 2 -x^3 + x^23 - 12x^8 + 45 x ^ 6 -x^47')
   print(poly_6)
   poly_7 = Polynomial('2x^5 - 71x^3 + 8x^2 - 93x^4 -6x + 192')
   poly_8 = Polynomial('192 -71x^3 + 8x^2 + 2x^5 -6x - 93x^4')
   poly_9 = poly_7 + poly_8
   print(poly_7)
   print(poly_8)
   print(poly_9)
   print(poly_7 * poly_7)
   print(poly_7)
   print(poly_7 - poly_7)
   print(poly_7)
   print(poly_9 / poly_7)
   print(poly_9)
   print(poly_7)
   poly_10 = Polynomial('-11x^4 + 3x^2 + 7x + 9')
   poly_11 = Polynomial('5x^2 -8x - 6')
   poly_12 = poly_10 * poly_11
   print(poly_12)
   print(poly_12 / poly_10)
   print(poly_12 / poly_11)
   poly_13 = poly_6 * poly_7
   print(poly_13 / poly_6)
   print(poly_13 / poly_7)
                                
                                          

    
        

