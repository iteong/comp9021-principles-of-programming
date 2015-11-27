# LAB 5

# Description: Generates all 3 x 3 magic squares.
#
# Essentially written by Pang Luo for COMP9021

# The sum of each row, column and diagonal is necessarily equal to
# ((1 + 9) * 9 / 2) / 3 = 15.
# Denoting by c the value of the cell at the centre,
# adding up the two diagonals, the middle row and the middle column yields
# 15 * 4 = 45 + 3c, hence c = 5.

all_nonzero_digits = set(range(1, 10))
for a in range(1, 10):
    for b in range(1, 10):
        candidate = (a        , 15 - a - b, b        ,
                     5 + b - a, 5         , 5 + a - b,
                     10 - b   , a + b - 5 , 10 - a   )
        if set(candidate) == all_nonzero_digits:
            print('  {:}  {:}  {:}\n  {:}  {:}  {:}\n  {:}  {:}  {:}\n'.format(*candidate))


# Extracts titles from a front page of the Sydney Morning Herald.
#
# Written by Eric Martin for COMP9021

import re


def extract_text(line, pattern):
    extracted_text = pattern.search(line)
    if extracted_text:
        title = extracted_text.groups()[0]
        print(title.replace('&nbsp;', ''))

# We look for text of the form title=....>TITLE</a></h3>
full_title_pattern = re.compile('title=[^>]*>([^<]*)</a></h3>')
# In some cases, </a></3> is at the beginning of the next line
title_at_end_of_line_pattern = re.compile('[^>]*>([^<]*)\n$')
end_tags_at_start_of_next_line_pattern = re.compile('^</a></h3>')

file = open('SMH.txt', 'r')
line = file.readline()
for next_line in file:
    if end_tags_at_start_of_next_line_pattern.search(next_line):
        extract_text(line, title_at_end_of_line_pattern)
    else:
        extract_text(line, full_title_pattern)
    line = next_line
# Process last line in the unique possible way
extract_text(line, full_title_pattern)
file.close()


# LAB 6

# Prompts the user for an amount, and outputs the minimal number of banknotes needed to match that amount,
# as well as the detail of how many banknotes of each type value are used.
# The available banknotes have a face value which is one of $1, $2, $5, $10, $20, $50, and $100.
#
# Written by Eric Martin for COMP9021

face_values = [1, 2, 5, 10, 20, 50, 100]
amount = int(input('Input the desired amount: '))

banknotes = []
amount_left = amount
while amount_left:
    value = face_values.pop()
    if amount_left >= value:
        banknotes.append((value, amount_left // value))
        amount_left %= value
nb_of_banknotes = sum(banknote[1] for banknote in banknotes)
if nb_of_banknotes == 1:
    print('\n1 banknote is needed.')
else:
    print('\n{:} banknotes are needed'.format(nb_of_banknotes))
print('The detail is:')
for banknote in banknotes:
    print('{:>4}: {:}'.format('$' + str(banknote[0]), banknote[1]))
    

# Prompts the user for the face values of banknotes and their associated quantities
# as well as for an amount, and if possible, outputs the minimal number of banknotes
# needed to match that amount, as well as the detail of how many banknotes of each type value are used.
#
# Written by Eric Martin for COMP9021


def print_solution(solution):
    max_width = max([len(str(value)) for value in solution]) + 1
    for value in sorted(solution.keys()):
        print('{:>{:}}: {:}'.format('$' + str(value), max_width, solution[value]))

            
print("Input pairs of the form 'value : number'\n"
      "   to indicate that you have 'number' many banknotes of face value 'value'.")
print('Input these pairs one per line, with a blank line to indicate end of input.\n')
face_values = []
while True:
    line = input()
    if ':' not in line:
        break
    value, quantity = line.split(':')
    face_values.append((int(value), int(quantity)))
# Might make the computation more efficient.
face_values.sort(reverse = True)
nb_of_face_values = len(face_values)
amount = int(input('Input the desired amount: '))

# minimal_combinations[sub_amount] will be a pair whose first element is the minimal number of banknotes
# needed to yield sub_amount, and whose second element is the list of all possible solutions,
# each solution being a dictionary with face values as keys and number of banknotes used as values.
minimal_combinations = [[0, []]] + [[float('inf'), []] for i in range(amount)]
for sub_amount in range(1, amount + 1):
    for i in range(nb_of_face_values):
        value = face_values[i][0]
        if sub_amount < value:
            continue
        if value == sub_amount:
            minimal_combinations[sub_amount] = [1, [{value : 1}]]
            continue
        # Using "value" to get "sub_amount" would require most banknotes that the minimum
        # number of banknotes so far found out to sum up to "sub_amount".
        if minimal_combinations[sub_amount - value][0] >= minimal_combinations[sub_amount][0]:
            continue
        for option in minimal_combinations[sub_amount - value][1]:
            # A banknote with face value "value" is available to complete "option" and result in a sum of "sub_amount".
            if value not in option or option[value] < face_values[i][1]:
                # Moreover, it determines a new minimum to then umber of banknotes that can sum of to "sub_amount".
                if minimal_combinations[sub_amount - value][0] + 1 < minimal_combinations[sub_amount][0]:
                    minimal_combinations[sub_amount][0] = minimal_combinations[sub_amount - value][0] + 1
                    minimal_combinations[sub_amount][1].clear()
                extended_option = dict(option)
                if value not in option:
                    extended_option[value] = 1
                else:
                    extended_option[value] += 1
                if extended_option not in minimal_combinations[sub_amount][1]:
                    minimal_combinations[sub_amount][1].append(extended_option)
minimal_nb_of_banknotes = minimal_combinations[amount][0]
if minimal_nb_of_banknotes == float('inf'):
    print('\nThere is no solution.')
else:
    solutions = minimal_combinations[amount][1]
    nb_of_solutions = len(solutions)
    if nb_of_solutions == 1:
        print('\nThere is a unique solution:')
        print_solution(solutions[0])
    else:
        print('\nThere are {:} solutions:'.format(nb_of_solutions))
        for i in range(nb_of_solutions - 1):
            print_solution(solutions[i])
            print()
        print_solution(solutions[nb_of_solutions - 1])
        

# A class to create fractions and work precisely with them.
#
# Written by Eric Martin for COMP9021

class Fraction():
    def __init__(self, *args):
        try:
            if len(args) != 2:
                raise TypeError
            if not self._validate(*args):
                raise ValueError
        except TypeError:
            print('Provide exactly two arguments.')
        except ValueError:
            print('Provide an integer and a nonzero integer as arguments.')
        else:
            self._set_to_normal_form(*args)
    
    def _validate(self, numerator, denominator):
        if type(numerator) is not int:
            return False
        if type(denominator) is not int:
            return False
        if denominator == 0:
            return False
        return True

    def _set_to_normal_form(self, numerator, denominator):
        if numerator * denominator < 0:
            sign = -1
        else:
            sign = 1
        numerator = abs(numerator)
        denominator = abs(denominator)
        gcd = self._gcd(numerator, denominator)
        self.numerator = sign * numerator // gcd
        self.denominator = denominator // gcd

    def _gcd(self, a, b):
        if b == 0:
            return a
        return self._gcd(b, a % b)

    def __repr__(self):
        return 'Fraction(numerator = {:}, denominator = {:})'.format(self.numerator, self.denominator)

    def __str__(self):
        return '{:} / {:}'.format(self.numerator, self.denominator)
        
    def __add__(self, fraction):
        return Fraction(self.numerator * fraction.denominator + self.denominator * fraction.numerator,
                        self.denominator * fraction.denominator)

    def __sub__(self, fraction):
        return Fraction(self.numerator * fraction.denominator - self.denominator * fraction.numerator,
                        self.denominator * fraction.denominator)

    def __mul__(self, fraction):
        return Fraction(self.numerator * fraction.numerator,  self.denominator * fraction.denominator)

    def __truediv__(self, fraction):
        try:
            if fraction.numerator == 0:
                raise ValueError
        except ValueError:
            print('Cannot divide by 0.')
        else:
            return Fraction(self.numerator * fraction.denominator,  self.denominator * fraction.numerator)

    def __lt__(self, fraction):
        return self.numerator * fraction.denominator < self.denominator * fraction.numerator

    def __le__(self, fraction):
        return self.numerator * fraction.denominator <= self.denominator * fraction.numerator

    def __gt__(self, fraction):
        return self.numerator * fraction.denominator > self.denominator * fraction.numerator

    def __ge__(self, fraction):
        return self.numerator * fraction.denominator >= self.denominator * fraction.numerator

    def __eq__(self, fraction):
        return self.numerator * fraction.denominator == self.denominator * fraction.numerator

    def __ne__(self, fraction):
        return self.numerator * fraction.denominator != self.denominator * fraction.numerator

    
    # LAB 7

    # Prompts the user for two numbers, say available_digits and desired_sum, and
# outputs the number of ways of selecting digits from available_digits
# that sum up to desired_sum.
#
# Written by Eric Martin for COMP9021


def solve(available_digits, desired_sum):
    if desired_sum < 0:
        return 0
    if available_digits == 0:
        if desired_sum == 0:
            return 1
        else:
            return 0
    # Either take the last digit d form available_digits and try to get desired_sum - d
    # from the remaining digits, or do not take the last digit and
    # try to get desired_sum from the remaining digits.
    return solve(available_digits // 10, desired_sum) + solve(available_digits // 10, desired_sum - available_digits % 10)

available_digits = int(input('Input a number that we will use as available digits: '))
desired_sum = int(input('Input a number that represents the desired sum: '))

nb_of_solutions = solve(available_digits, desired_sum)
if nb_of_solutions == 0:
    print('There is no solution.')
elif nb_of_solutions == 1:
    print('There is a unique solution')
else:
    print('There are {:} solutions.'.format(nb_of_solutions))


# Say that two strings s_1 and s_2 can be merged into a third
# string s_3 if s_3 is obtained from s_1 by inserting
# arbitrarily in s_1 the characters in s_2, respecting their
# order. For instance, the two strings ab and cd can be merged
# into abcd, or cabd, or cdab, or acbd, or acdb..., but not into
# adbc nor into cbda.
#
# Prompts the user for 3 strings and displays the output as follows:
# - If no string can be obtained from the other two by merging,
# then the program outputs that there is no solution.
# - Otherwise, the program outputs which of the strings can be obtained
# from the other two by merging.
#
# Written by Eric Martin for COMP9021


def can_merge(string_1, string_2, string_3):
    if not string_1 and string_2 == string_3:
        return True
    if not string_2 and string_1 == string_3:
        return True
    if not string_1 or not string_2:
        return False
    if string_1[0] == string_3[0] and can_merge(string_1[1: ], string_2, string_3[1: ]):
        return True
    if string_2[0] == string_3[0] and can_merge(string_1, string_2[1: ], string_3[1: ]):
        return True
    return False

strings = []
ordinals = ('first', 'second', 'third')
for i in ordinals:
    strings.append(input('Please input the {:} string: '.format(i)))

last = 0
if len(strings[1]) > len(strings[0]):
        last = 1
if len(strings[2]) > len(strings[last]):
    last = 2
if last == 0:
    first, second = 1, 2
elif last == 1:
    first, second = 0, 2
else:
    first, second = 0, 1
if len(strings[last]) != len(strings[first]) + len(strings[second]) or not can_merge(strings[first], strings[second], strings[last]):
    print('No solution')
else:
    print('The {:} string can be obtained by merging the other two.'.format(ordinals[last]))


# LAB 8

# A Doubly Linked List abstract data type
#
# Written by Eric Martin for COMP9021


class Node:
    def __init__(self, value = None):
        self.value = value
        self.next_node = None
        self.previous_node = None


class DoublyLinkedList:
    # Creates a linked list possibly from a list of values.
    def __init__(self, L = None):
        if not L:
            self.head = None
            return
        node = Node(L[0])
        self.head = node
        for e in L[1: ]:
            node.next_node = Node(e)
            node.next_node.previous_node = node
            node = node.next_node

    def print(self, separator = ', '):
        if not self.head:
            return
        node = self.head
        print(node.value, end = '')
        node = node.next_node
        while node:
            print(separator, node.value, sep = '', end = '')
            node = node.next_node
        print()

    def duplicate(self):
        if not self.head:
            return None
        node = self.head
        node_copy = Node(node.value)
        LL = DoublyLinkedList()
        LL.head = node_copy
        node = node.next_node
        while node:
            node_copy.next_node = Node(node.value)
            node_copy.next_node.previous_node = node_copy
            node_copy = node_copy.next_node
            node = node.next_node
        return LL

    def length(self):
        if not self.head:
            return 0
        node = self.head
        length = 1
        node = node.next_node
        while node:
            length +=1
            node = node.next_node
        return length

    def apply_function(self, function):
        node = self.head
        while node:
            node.value = function(node.value)
            node = node.next_node

    def is_sorted(self, comparison_function = lambda x, y: x <= y):
        node = self.head
        while node and node.next_node:
            if not comparison_function(node.value, node.next_node.value):
                return False
            node = node.next_node
        return True

    def extend(self, LL):
        if not self.head:
            self.head = LL.head
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = LL.head
        LL.head.previous_node = node

    def reverse(self):
        if not self.head or not self.head.next_node:
            return
        node = self.head
        while node.next_node.next_node:
            node = node.next_node
        last_node = node.next_node
        node.next_node = None
        self.reverse()
        last_node.next_node = self.head
        self.head.previous_node = last_node
        self.head = last_node

    def index_of_value(self, value):
        index = 0
        node = self.head
        while node:
            if node.value == value:
                return index
            index += 1
            node = node.next_node
        return -1

    def value_at(self, index):
        if index < 0:
            return None
        node = self.head
        while node and index:
            node = node.next_node
            index -= 1
        if node and index == 0:
            return node.value
        return None

    def prepend(self, LL):
        if not LL.head:
            return
        node = LL.head
        while node.next_node:
            node = node.next_node
        node.next_node = self.head
        self.head.previous_node = node
        self.head = LL.head
            
    def append(self, value):
        if not self.head:
            self.head = Node(value)
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = Node(value)
        node.next_node.previous_node = node

    def insert_value_at(self, value, index):
        new_node = Node(value)
        if index <= 0:
            new_node.next_node = self.head
            if self.head:
                self.head.previous_node = new_node
            self.head = new_node
            return
        if not self.head:
            self.head = new_node
        node = self.head
        while node.next_node and index > 1:
            node = node.next_node
            index -= 1
        next_node = node.next_node
        node.next_node= new_node
        new_node.previous_node = node
        new_node.next_node = next_node
        if next_node:
            next_node.previous_node = new_node

    def insert_value_before(self, value_1, value_2):
        if not self.head:
            return False
        if self.head.value == value_2:
            self.insert_value_at(value_1, 0)
            return True
        node = self.head
        while node.next_node and node.next_node.value != value_2:
            node = node.next_node
        if not node.next_node:
            return False
        new_node = Node(value_1)
        new_node.next_node = node.next_node
        if node.next_node:
            node.next_node.previous_node = new_node
        node.next_node = new_node
        new_node.previous_node = node
        return True

    def insert_value_after(self, value_1, value_2):
        if not self.head:
            return False
        node = self.head
        while node and node.value != value_2:
            node = node.next_node
        if not node:
            return False
        new_node = Node(value_1)
        new_node.next_node = node.next_node
        if node.next_node:
            node.next_node.previous_node = new_node
        node.next_node = new_node
        new_node.previous_node = node
        return True

    def insert_sorted_value(self, value, comparison_function = lambda x, y: x <= y):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        if comparison_function(value, self.head.value):
            new_node.next_node = self.head
            self.head.previous_node = new_node
            self.head = new_node
            return
        node = self.head
        while node.next_node and comparison_function(node.next_node.value, value):
            node = node.next_node
        new_node.next_node = node.next_node
        if node.next_node:
            node.next_node.previous_node = new_node
        node.next_node = new_node
        new_node.previous_node = node

    def delete_value(self, value):
        if self.head and self.head.value == value:
            self.head = self.head.next_node
            return True
        node = self.head
        while node.next_node and node.next_node.value != value:
            node = node.next_node
        if node.next_node:
            node.next_node = node.next_node.next_node
            if node.next_node:
                node.next_node.previous_node = node
            return True
        return False
            

if __name__ == '__main__':
    LL = DoublyLinkedList([2, 0, 1, 3, 7])
    LL.print(separator = ' : ')
    LL_copy = LL.duplicate()    
    LL_copy.print()
    print(LL.length())
    LL.apply_function(lambda x: 2 * x)
    LL.print()
    print(LL.is_sorted(lambda x, y: x <= y))
    LL.extend(LL_copy)
    LL.print()
    LL.reverse()
    LL.print()
    print(LL.index_of_value(2))
    print(LL.index_of_value(5))
    print(LL.value_at(4))
    print(LL.value_at(10))
    LL.prepend(DoublyLinkedList([20, 21, 22]))
    LL.print()
    LL_1 = DoublyLinkedList()
    LL_1.print()
    LL_1.append(10)
    LL_1.print()
    LL_1.append(15)
    LL_1.print()
    LL_1.insert_value_at(5, 0)
    LL_1.insert_value_at(25, 3)
    LL_1.insert_value_at(20, 3)
    LL_1.print()
    LL_1.insert_value_before(0, 5)
    LL_1.insert_value_before(30, 35)
    LL_1.insert_value_before(22, 25)
    LL_1.insert_value_before(7, 10)
    LL_1.print()
    LL_1.insert_value_after(3, 1)
    LL_1.insert_value_after(2, 0)
    LL_1.insert_value_after(12, 10)
    LL_1.insert_value_after(27, 25)
    LL_1.print()
    LL_1.insert_sorted_value(-5)
    LL_1.insert_sorted_value(17)
    LL_1.insert_sorted_value(30)
    LL_1.print()
    LL_1.delete_value(-5)
    LL_1.delete_value(30)
    LL_1.delete_value(15)
    LL_1.print()
    
    
# LAB 9

# Uses the Stack interface to evaluate an arithmetic expression
# written in infix, fully parenthesised with parentheses, brackets and braces,
# and built from natural numbers using the binary +, -, * and / operators.             
#
# Written by Eric Martin for COMP9021

from array_stack import *

class FullyParenthesisedExpression():
    def __init__(self, expression = None):
        self.expression = expression
        self.list_of_tokens = []
        if not self.get_list_of_tokens(self.list_of_tokens):
            print('Invalid expression')
            return
        self.stack = ArrayStack()

    def get_list_of_tokens(self, list_of_tokens):
        reading_number = False
        for c in self.expression:
            if c.isdigit():
                if not reading_number:
                    reading_number = True
                    number = int(c)
                else:
                    number = number * 10 + int(c)
            else:
                if reading_number:
                    list_of_tokens.append(number)
                    reading_number = False
                if c in '+-*/()[]{}':
                    list_of_tokens.append(c)
                elif c != ' ':
                    return False
        if reading_number:
            list_of_tokens.append(number)
        return True
                    
    def evaluate(self):
        for token in self.list_of_tokens:
            if token in list('+-*/([{'):
                self.stack.push(token)
            elif isinstance(token, int):
                self.stack.push(token)
            else:
                try:
                    second_argument = self.stack.pop()
                    operator = self.stack.pop()
                    first_argument = self.stack.pop()
                    opening_grouping_symbol = self.stack.pop()
                    if token == ')' and opening_grouping_symbol != '(' or \
                       token == ']' and opening_grouping_symbol != '[' or \
                       token == '}' and opening_grouping_symbol != '{':                   
                        raise Exception
                except:
                    print('Incorrect expression.')
                    return None
                if operator == '+':
                    self.stack.push(first_argument + second_argument)
                elif operator == '-':
                    self.stack.push(first_argument - second_argument)
                elif operator == '*':
                    self.stack.push(first_argument * second_argument)
                elif operator == '/' and second_argument:
                    self.stack.push(first_argument / second_argument)
                else:
                    print('Division by 0.')
                    return None
        if self.stack.is_empty():
            print('Incorrect expression.')
            return None
        result = self.stack.pop()
        if not self.stack.is_empty():
            print('Incorrect expression.')
            return None
        return result


if __name__ == '__main__':
    print('Testing 2:')
    fully_parenthesised_expression = FullyParenthesisedExpression('2')
    print(fully_parenthesised_expression.evaluate())
    print('Testing (2 + 3):')
    fully_parenthesised_expression = FullyParenthesisedExpression('(2 + 3)')
    print(fully_parenthesised_expression.evaluate())
    print('Testing [(2 + 3) / 10]:')
    fully_parenthesised_expression = FullyParenthesisedExpression('[(2 + 3) / 10]')
    print(fully_parenthesised_expression.evaluate())
    print('Testing (12 + [{[13 + (4 + 5)] - 10} / (7 * 8)]):')
    fully_parenthesised_expression = FullyParenthesisedExpression('(12 + [{[13 + (4 + 5)] - 10} / (7 * 8)])')
    print(fully_parenthesised_expression.evaluate())

# LAB 10

# Reads from a file named tree.txt, containing numbers expected to be organised as a tree,
# a number at a depth of N in the tree being preceded with N tabs in the file.
# The file can also contain any number of lines with nothing but blank lines.
# Uses the module general_tree.py to build the tree represented in the file
# (outputs an error message in case the representation is incorrect),
# and prints it out using the same representation as in the file.
#
# Written by Eric Martin for COMP9021


import sys
from general_tree import *


def generate_nonblank_lines(input_file):
    nonblank_lines = []
    for line in input_file:
        line = line.rstrip()
        if line:
            nonblank_lines.append(line)
    nonblank_lines.reverse()
    return nonblank_lines

def number_of_leading_tabs(line):
    count = 0
    while count < len(line) and line[count] == '\t':
        count += 1
    return count

def build_tree(input_file):
    lines = generate_nonblank_lines(input_file)
    if not lines or number_of_leading_tabs(lines[-1]):
        return None
    tree = _build_tree(lines, 0)
    if not tree or lines:
        return None
    return tree

def _build_tree(lines, level):
    line = lines.pop()
    try:
        value = int(line[level: ])
    except:
        return None
    tree = GeneralTree(value)   
    while lines:
        next_line_level = number_of_leading_tabs(lines[-1])
        if next_line_level > level + 1:
            return None
        if next_line_level == level + 1:
            tree.children.append(_build_tree(lines, level + 1))
        else:
            return tree
    return tree
                
def print_out(tree):
    _print_out(tree, 0)

def _print_out(tree, level):
    print('\t' * level, end = '')
    print(tree.value)
    for subtree in tree.children:
        _print_out(subtree, level + 1)
        
        
try:
    input_file = open('tree.txt', 'r')
except:
    print('Sorry, could not open file tree.txt.')
    sys.exit()
    
tree = build_tree(input_file)
if not tree:
    print('tree.txt does not contain the correct representation of a tree.')
    sys.exit()
print_out(tree)


# LAB 11

# Defines a class to manage a list of values with the following operations:
# - add a value in logarithmic time complexity;
# - delete the smallest value, delete the largest value in constant time complexity;
# - return the median in constant time complexity.
#
# Written by Eric Martin for COMP9021

from priority_queue import *

class Median:
    def __init__(self):
        # To store the first half of the values, the largest of which is of highest priority
        self.max_pq = MaxPriorityQueue()
        # To store the second half of the values, the smallest of which is of highest priority
        self.min_pq = MinPriorityQueue()

    def nb_of_elements(self):
        return len(self.max_pq) + len(self.min_pq)

    def median(self):
        if len(self.max_pq) > len(self.min_pq):
            return self.max_pq.top_priority()
        if len(self.min_pq) > len(self.max_pq):
            return self.min_pq.top_priority()
        return (self.max_pq.top_priority() + self.min_pq.top_priority()) / 2

    def insert(self, element):
        # Do not bother with two many cases in case we are adding the second element:
        # let it join the side with the first element and let rebalance() make sure
        # that both elements end up on the correct side.       
        if self.max_pq.top_priority() == None:
            self.min_pq.insert(element)
            self._rebalance()
        elif self.min_pq.top_priority() == None:
            self.max_pq.insert(element)
            self._rebalance()
        elif element < self.max_pq.top_priority():
            self.max_pq.insert(element)
            self._rebalance()
        elif element > self.min_pq.top_priority():
            self.min_pq.insert(element)
            self._rebalance()
        # In both cases, "element" is equal to the largest element from the first half
        # and to the smallest element from the second half, so it can join either side.
        # We chose a side so as to avoid rebalance.
        elif len(self.max_pq) <= len(self.min_pq):
            self.max_pq.insert(element)
        else:
            self.min_pq.insert(element)
            
    def _rebalance(self):
        if len(self.min_pq) > len(self.max_pq) + 1:
            self.max_pq.insert(self.min_pq.delete_top_priority())
        elif len(self.max_pq) > len(self.min_pq) + 1:
            self.min_pq.insert(self.max_pq.delete_top_priority())

if __name__ == '__main__':
    L = [2, 1, 7, 5, 4, 8, 0, 6, 3, 9]
    values = Median()
    for e in L:
        values.insert(e)
        print(values.median(), end = ' ')
    print()
        

# A max or min priority queue abstract data type.
#
# Written by Eric Martin for COMP9021


MIN_CAPACITY = 10


# Max priority queue by default
class PriorityQueue():
    def __init__(self, capacity = MIN_CAPACITY, compare = lambda x, y: x > y):
        self._data = [None] * capacity
        self._length = 0
        self._compare = compare
        
    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def top_priority(self):
        if not self._length:
            return None
        return self._data[1]

    def insert(self, element):
        if self._length + 1 == len(self._data):
            self._resize(2 * len(self._data))
        self._length += 1
        self._data[self._length] = element
        self._bubble_up(self._length)

    def delete_top_priority(self):
        top_element = self._data[1]
        self._data[1], self._data[self._length] = self._data[self._length], self._data[1]
        self._length -= 1
        if MIN_CAPACITY * 2 <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        self._bubble_down(1)
        return top_element

    def _bubble_up(self, i):
        if i > 1 and self._compare(self._data[i], self._data[i // 2]):
            self._data[i // 2], self._data[i] = self._data[i], self._data[i // 2]
            self._bubble_up(i // 2)

    def _bubble_down(self, i):
        child = 2 * i
        if child < self._length and self._compare(self._data[child + 1], self._data[child]):
            child += 1
        if child <= self._length:
            if self._compare(self._data[child], self._data[i]):
                self._data[child], self._data[i] = self._data[i], self._data[child]
                self._bubble_down(child)

    def _resize(self, new_size):
        self._data = list(self._data[ : self._length + 1]) + [None] * (new_size - self._length - 1)


class MaxPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()
        

class MinPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__(compare = lambda x, y: x < y)
        


        
if __name__ == '__main__':
    max_pq = MaxPriorityQueue()
    min_pq = MinPriorityQueue()
    L = [13, 13, 4, 15, 9, 4, 5, 14, 4, 11, 15, 2, 17, 8, 14, 12, 9, 5, 6, 16]
    for e in L:
        max_pq.insert(e)
        min_pq.insert(e)
    print(max_pq._data[ : max_pq._length + 1])
    print(min_pq._data[ : min_pq._length + 1])
    for i in range(len(L)):
        print(max_pq.delete_top_priority(), end = ' ')
    print()
    for i in range(len(L)):
        print(min_pq.delete_top_priority(), end = ' ')
    print()        

# A max priority queue abstract data type to insert pairs of the form (datum, priority).
# If a pair is inserted with a datum that already occurs in the priority queue, then
# the priority is (possibly) changed to the (possibly) new value.
#
# Written by Eric Martin for COMP9021


MIN_CAPACITY = 10


class PriorityQueue():
    def __init__(self, capacity = MIN_CAPACITY):
        self._data = [None] * capacity
        self._length = 0
        self._locations = {}
        
    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def insert(self, element):
        datum = element[0]
        priority = element[1]
        if datum in self._locations:
            self._change_priority(datum, priority)
            return
        if self._length + 1 == len(self._data):
            self._resize(2 * len(self._data))
        self._length += 1
        self._data[self._length] = [datum, priority]
        self._locations[datum] = self._length
        self._bubble_up(self._length)

    def delete(self):
        top_datum = self._data[1][0]
        del self._locations[top_datum]        
        self._data[1], self._data[self._length] = self._data[self._length], self._data[1]
        self._length -= 1
        if MIN_CAPACITY <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        self._bubble_down(1)
        return top_datum

    def _change_priority(self, datum, priority):
        i = self._locations[datum]
        if priority > self._data[i][1]:
            self._data[i][1] = priority
            self._bubble_up(i)
        elif priority < self._data[i][1]:
            self._data[i][1] = priority
            self._bubble_down(i)
            self._bubble_up(i)
        
    def _bubble_up(self, i):
        if i > 1 and self._data[i][1] > self._data[i // 2][1]:
            self._data[i // 2], self._data[i] = self._data[i], self._data[i // 2]
            self._locations[self._data[i // 2][0]] = i // 2
            self._locations[self._data[i][0]] = i
            self._bubble_up(i // 2)

    def _bubble_down(self, i):
        child = 2 * i
        if child < self._length and self._data[child + 1][1] > self._data[child][1]:
            child += 1
        if child <= self._length and self._data[child][1] > self._data[i][1]:
            self._data[child], self._data[i] = self._data[i], self._data[child]
            self._locations[self._data[child][0]] = child
            self._locations[self._data[i][0]] = i
            self._bubble_down(child)

    def _resize(self, new_size):
        self._data = list(self._data[ : self._length + 1]) + [None] * (new_size - self._length - 1)
        

if __name__ == '__main__':
    pq = PriorityQueue()
    L = [('A', 13), ('B', 13), ('C', 4), ('D', 15), ('E', 9), ('F', 4), ('G', 5), ('H', 14),
         ('A', 4), ('B', 11), ('C', 15), ('D', 2), ('E', 17),
         ('A', 8), ('B', 14), ('C',12), ('D', 9), ('E', 5),
         ('A', 6), ('B', 16)]
    for e in L:
        pq.insert(e)
    for i in range(8):
        print(pq.delete(), end = ' ')
    print()
    print(pq.is_empty())
    
   
            