reverse(e, List, List).
reverse(l(First, Rest), Result, Accumulator) :- reverse(Rest, Result, l(First, Accumulator)).

is_palindrome(List) :- reverse(List, List, e).
  
