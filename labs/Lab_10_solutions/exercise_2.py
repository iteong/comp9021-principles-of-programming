# Uses the Stack and the BinaryTree interfaces to build an expression tree and evaluate
# an arithmetic expression written in infix, fully parenthesised with parentheses, brackets and braces,
# and built from natural numbers using the binary +, -, * and / operators.             
#
# Written by Eric Martin for COMP9021

from array_stack import *
from binary_tree import *

class FullyParenthesisedExpression():
    def __init__(self, expression = None):
        self.expression = expression
        self.list_of_tokens = []
        if not self.get_list_of_tokens(self.list_of_tokens):
            print('Invalid expression')
            return
        self.stack = ArrayStack()
        self.expression_tree = self.build_expression_tree()
        if not self.expression_tree:
            print('Invalid expression')

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
                    
    def build_expression_tree(self):
        for token in self.list_of_tokens:
            if token in list('+-*/([{'):
                self.stack.push(token)
            elif isinstance(token, int):
                self.stack.push(BinaryTree(token))
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
                    return None
                tree = BinaryTree()
                tree.value = operator
                tree.left_node = first_argument
                tree.right_node = second_argument
                self.stack.push(tree)
        if self.stack.is_empty():
            return None
        tree = self.stack.pop()
        if not self.stack.is_empty():
            return None
        return tree

    def evaluate(self):
        return self._evaluate(self.expression_tree)
    
    def _evaluate(self, tree):
        if isinstance(tree.value, int):
            return tree.value
        first_argument = self._evaluate(tree.left_node)
        second_argument = self._evaluate(tree.right_node)
        if first_argument == None or second_argument == None:
            return None
        if tree.value == '+':
            return first_argument + second_argument
        if tree.value == '-':
            return first_argument + second_argument
        if tree.value == '*':
            return first_argument * second_argument
        if tree.value == '/':
            if second_argument == 0:
                print('Division by 0')
                return None
            return first_argument / second_argument


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
    
