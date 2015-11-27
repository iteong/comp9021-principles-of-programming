# Prompts the user for input and checks whether it is a palindrome.
#
# Written by Eric Martin for COMP9021

def palindrome():
    text = input('Input some text: ')

    print('"', text, '"', sep = '', end = ' ')
    while len(text) > 1:
        start, *text, end = text
        if start != end:
            print('is not a palindrome.')
            return
    print('is a palindrome.')


if __name__ == '__main__':
    palindrome()
