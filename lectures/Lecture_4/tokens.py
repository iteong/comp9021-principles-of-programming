def extract_tokens(word): # "p(f(a,g(asd,h))"
    word = ''.join(word.split()) # erase the spaces, get rid of white spaces
    list_of_tokens = []
    token =''
    count_of_nonclosed_opening_parentheses = 0
    for c in word:
        if c == ',':
            if count_of_nonclosed_opening_parentheses == 0:
                list_of_tokens.append(token)
                token = ''
            else:
                token += ','
        elif c == '(':
            count_of_nonclosed_opening_parentheses += 1
            token += '('
        elif c == ')':
            count_of_nonclosed_opening_parentheses -= 1
            token += ')'
        else:
            token += c
    list_of_tokens.append(token)
    return list_of_tokens

# line.split: get rid of head and body
