from array_stack import *

class BalancedExpression:
    def __init__(self, input_string):
        self.input_string = input_string

    def is_balanced(self):
        symbols_to_check = '{}[]()'
        opening_symbols_to_check = '{[('
        stack = ArrayStack()
        for c in self.input_string:
            if c not in symbols_to_check:
                continue
            if c in opening_symbols_to_check:
                stack.push(c)
            else:
                if stack.is_empty():
                    print('Not balanced')
                    return
                if c == '}':
                    if stack.pop() != '{':
                        print('Not balanced')
                        return
                if c == ']':
                    if stack.pop() != '[':
                        print('Not balanced')
                        return
                if c == ')':
                    if stack.pop() != '(':
                        print('Not balanced')
                        return
            if not stack.is_empty():
                print('Not balanced')
                return
            print('Balanced!')
