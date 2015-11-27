def encodes_set_as_an_int(a_set):
    encoding = 0 #zero codes the empty set
    for i in a_set:
        encoding += 1<<i #push 1 to the left
    return encoding

#look at bit_set.py
        
