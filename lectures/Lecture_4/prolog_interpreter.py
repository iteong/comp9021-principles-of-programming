# A (much too) limited Prolog parser and interpreter.
#
# Written by Eric Martin for COMP9021


def get_program(file_name):
    '''Reads the contents of a file containing a Prolog program, and allows the user to
    store it as a dictionnary, representing each atom as a string with all spaces removed,
    and where for each rule,
    - the head of the rule is a key of the dictionnary;
    - the list of conjuncts of the body of the rule is the value
      of the dictionnary for the corresponding key.
    Different clauses are assumed to have different heads.
    The bodies of the rules are restricted to conjunctions of atoms
    (no disjunction, no negation, no identity, no cut...).
    The terms are built from function symbols of a given arity.
    So for example, we can use a constant e and a binary function symbol l
    so that the list (2, 3, 4, 5) can be represented as f(2, f(3, f(4, f(5, e))))
    (which in standard Prolog, is represented as [2| [3| [4| [5| []]]]]).
    The bodies of the rules are assumed to contain no variable which does not occur
    in the head of the rule (a very strong restriction...).
    The program is supposed to be syntactically correct, no check is performed.
    '''
    type_file = open(file_name, 'r')
    program = {}
    for line in type_file.readlines():
        # Get rid of all whitespace in the clause and the full stop at the end.
        line = ''.join(line.split()).strip('.')
        if not line:
            continue
        clause = line.split(':-')
        head = clause[0]
        if len(clause) == 1:
            body = []
        else:
            body = parse(clause[1])
        program[head] = body
    return program

def parse(expression, break_atom = False):
    '''When break_atom is False, it is meant to return the list of atoms
    in the body of a clause, represented as a string where those atoms are separated by commas.
    When break_atom is True, it is meant to return a list consisting of a function symbol f
    and terms t_1, ..., t_n from a string representing the term f(t_1,...,t_n).
    The expression is supposed to be syntactically correct, no check is performed.

    >>> parse('reverse(l(First, Rest), Result, Accumulator)')
    ['reverse(l(First, Rest), Result, Accumulator)']
    
    >>> parse('reverse(l(First, Rest), Result, Accumulator)', True)
    ['reverse', 'l(First, Rest)', ' Result', ' Accumulator']
    '''
    words = []
    word = ''
    count_of_non_closed_opening_parentheses = 0
    for c in expression:
        if c == ',' and (count_of_non_closed_opening_parentheses == 0 or
                         break_atom and count_of_non_closed_opening_parentheses == 1):
            words.append(word)
            word = ''
        elif c == '(':
            if break_atom and count_of_non_closed_opening_parentheses == 0:
                words.append(word)
                word = ''
            else:                
                word += '('
            count_of_non_closed_opening_parentheses += 1
        elif c == ')':
            count_of_non_closed_opening_parentheses -= 1
            if count_of_non_closed_opening_parentheses or not break_atom:
                    word += ')'
        else:
            word += c
    if word:
        words.append(word)
    return words

def unify(expression_1, expression_2, unification = None):
    '''Unifies two atoms or terms at most one of which contains variables
    (that is, capitalised terms, but contrary to standard Prolog underscores are not allowed).
    The third argument is used to possibly record the assignment of some terms to some variables,
    which has to be consistently extended; it is what is eventually returned.
    
    >>> unify('a','a')
    {}
    
    >>> unify('a', 'b')

    >>> unify('a','X')
    {'X': 'a'}
    
    >>> d = unify('f(a,b,b,a)', 'f(X,Y,Z,X)'); sorted([(x, d[x]) for x in d])
    [('X', 'a'), ('Y', 'b'), ('Z', 'b')]

    >>> d = unify('f(a,f(a,b,g(c,d),f(a,g(c,d))))', 'f(X,f(a,Y,U,f(X,g(V,d))))'); sorted([(x, d[x]) for x in d])
    [('U', 'g(c,d)'), ('V', 'c'), ('X', 'a'), ('Y', 'b')]
    
    >>> unify('f(a,f(a,b,g(c,d),f(a,g(c,d))))', 'f(X,f(a,Y,U,f(X,g(Y,d))))')
    '''
    if unification == None:
        unification = {}
    if expression_1 == expression_2:
        return unification
    if expression_1[0].isupper():
        return unify_variable_with(expression_1, expression_2, unification)
    if expression_2[0].isupper():
        return unify_variable_with(expression_2, expression_1, unification)
    parsed_expression_1 = parse(expression_1, True)
    parsed_expression_2 = parse(expression_2, True)
    length = len(parsed_expression_1)
    if length != len(parsed_expression_2):
        return None
    if parsed_expression_1[0] != parsed_expression_2[0]:
        return None
    for i in range(1, length):
        if unify(parsed_expression_1[i], parsed_expression_2[i], unification) == None:
            return None
    return unification

def unify_variable_with(variable, expression, unification):
    '''Extends unification, if possible, and if necessary, by assigning expression to variable.'''
    if variable not in unification:
        unification[variable] = expression
    elif unification[variable] != expression:
        return None
    return unification

def unify_atoms(list_of_atoms, program):
    '''Given a list of closed atoms, initialised with the query, tries to unify
    the first atom in the list with the head of one of the rules of the program, and
    if successful, adds to the beginning of the list all atoms that make up the
    body of that rule, after substitution of all variables by closed terms according to the
    result of the unification.
    Returns True when the list of atoms becomes empty, and False when processing an atom
    that cannot be unified.'''
    if not list_of_atoms:
        return True
    for head in program:
        head_unification = unify(head, list_of_atoms[0])
        if head_unification != None:
            body = list(program[head])
            for i in range(len(body)):
                # To make sure that if a variable var_1 is an initial segment of a variable var_2,
                # then var_2 is processed before var_1;
                # otherwise, when substituting var_1 by a term, that term would not only replace
                # the variable var_1, but also var_1 as an initial segment of var_2.
                variables = reversed(sorted(list(head_unification.keys())))
                for variable in variables:
                    body[i] = body[i].replace(variable, head_unification[variable])
            body.extend(list_of_atoms[1:])
            if unify_atoms(body, program):
                return True
    return False

def answer_query(query, program):
    '''Answers yes or no to whether a closed query is a logical consequence of a Prolog program
    represented as a dictionnary thanks to a call to the function get_program().

    >>> program = {'a(X)' : ['b', 'c(X)', 'd(X)'],
    ...    'b' : [],
    ...	   'c(X)' : ['b'],
    ...	   'd(X)' : ['b', 'e(X)', 'f'],
    ...	   'e(X)' : [],
    ...	   'f' : ['c(X)'],
    ...	   'g(X)' : ['a(X)', 'h']}
    
    >>> answer_query('a(0)', program)
    True
    
    >>> answer_query('g(0)', program)
    False
    '''
    query = ''.join(query.split())
    print(unify_atoms([query], program))

