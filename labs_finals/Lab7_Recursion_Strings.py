strings = []
ordinals = ('first','second','third')
for i in ordinals:
    strings.append(input('Please input the {:} string: '.format(i)))

print('\nInputs in Strings List: {:}'.format(strings))


# Sorting strings: assign index values to variables to check particular string's index in list strings using length,
# so that these variables can be used in merge function to input strings where string3 is always
# the longest string
last = 0
if len(strings[1]) > len(strings[0]):
    last = 1
if len(strings[2]) > len(strings[last]):
    last = 2

if last == 0:
    first, second = 1, 2
elif last == 1:
    first, second = 0, 2
else: # last = 2
    first, second = 0, 1

print('\nFirst ordinal string "{:}" is index {:} in Strings list.'.format(strings[first], first))
print('Second ordinal string "{:}" is index {:} in Strings list.'.format(strings[second], second))
print('Last ordinal string "{:}" is index {:} in Strings list.'.format(strings[last], last))


def merge(string1, string2, string3):
    ## base cases
    # first base case: if string1 empty AND string2 = string3, merge = True!
    if not string1 and string2 == string3:
        return True
    # second base case: if string2 empty AND string1 = string3, merge = True!
    if not string2 and string1 == string3:
        return True
    ## if string1 and string2 empty (nothing to merge to give resulting string
    if not string1 and not string2:
        return False

    # if string1 has same first letter as string3 (i.e. ab, cd, abcd) , and
    # merge(string1's letters without 1st, string2, string3's letters without first) is True
    # (ab, cd, abcd) => (_b, cd, _bcd) => (_, cd, _cd) => hits first base case
    if string1[0] == string3[0] and merge(string1[1:], string2, string3[1:]):
        return True
    # (cd, ab, abcd) => (cd, _b, _bcd) => (cd, _, _cd) => hits second base case
    if string2[0] == string3[0] and merge(string1, string2[1:], string3[1:]):
        return True
    return False # otherwise if conditions not met, merge is False

# 2 substrings cannot be added up in length to give same length as longest string
if len(strings[last]) != len(strings[first]) + len(strings[second]):
    print('\nNo solution.')
# sorted strings in list cannot be merged
if not merge(strings[first], strings[second], strings[last]):
    print('\nNo solution.')
else: # 2 substrings can be added up in length to give resulting string and sorted strings can be merged
    print('\nThe {:} string can be obtained by merging the other two.'.format(ordinals[last]))




