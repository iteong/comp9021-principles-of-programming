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
    
