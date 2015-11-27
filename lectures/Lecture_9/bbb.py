from array_stack import *

class BalancedExpression:
    def __init__(self, input_string):
        self.input_string = input_string

    def evaluate(self):
        stack = ArrayStack()
        in_number = False
        for c in self.input_string:
            if c.isdigit():
                if in_number:
                    stack.push(stack.pop() * 10 + int(c))
                else:
                    in_number = True
                    stack.push(int(c))
            else:
                in_number = False
                if c == ' ':
                    continue
                if c not in '+*/-':
                    print('Bad')
                    return
                if c == '*':
                    stack.push(arg_1 * arg_2)
                if c == '+':
                    stack.push(arg_1 + arg_2)
                if c == '-':
                    stack.push(arg_1 - arg_2)
                if c == '/':
                    try:
                        stack.push(arg_1 / arg_2)
                    except:
                        print('Bad')
                        return
            if len(stack
