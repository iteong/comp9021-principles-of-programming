# Uses the Stack interface to evaluate an arithmetic expression
# written in postfix and built from natural numbers using the
# the binary +, -, * and / operators.             
#
# Written by Eric Martin for COMP9021

from array_stack import *

class PostfixExpression():
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
                if c in '+-*/':
                    list_of_tokens.append(c)
                elif c != ' ':
                    return False
        if reading_number:
            list_of_tokens.append(number)
        return True
                    
    def evaluate(self):
        for token in self.list_of_tokens:
            if isinstance(token, int):
                self.stack.push(token)
            else:
                try:
                    second_argument = self.stack.pop()
                    first_argument = self.stack.pop()
                except:
                    print('Incorrect postfix expression.')
                    return None
                if token == '+':
                    self.stack.push(first_argument + second_argument)
                elif token == '-':
                    self.stack.push(first_argument - second_argument)
                elif token == '*':
                    self.stack.push(first_argument * second_argument)
                elif second_argument:
                    self.stack.push(first_argument / second_argument)
                else:
                    print('Division by 0.')
                    return None
        if self.stack.is_empty():
            print('Incorrect postfix expression.')
            return None
        result = self.stack.pop()
        if not self.stack.is_empty():
            print('Incorrect postfix expression.')
        return result


if __name__ == '__main__':
    print('Testing 2:')
    postfix_expression = PostfixExpression('2')
    print(postfix_expression.evaluate())
    print('Testing 2 3+:')
    postfix_expression = PostfixExpression('2 3+')
    print(postfix_expression.evaluate())
    print('Testing 2 3+ 10  /:')
    postfix_expression = PostfixExpression('2 3+ 10  /')
    print(postfix_expression.evaluate())
    print('Testing 12 13 4 5+ + 10 -  7 8 * /+:')
    postfix_expression = PostfixExpression('12 13 4 5+ + 10 -  7 8 * /+')
    print(postfix_expression.evaluate())
    
