# Computes the hash code of a string as a 32 bit number
# that aggregates the ascii codes of all characters in the string,
# at each step shifting the resulting code by a given number.
#
# Written by Eric Martin for COMP9021


def hash_code(word, shift):
    mask = (1 << 32) - 1
    code = 0
    for c in word:       
        code = (code << shift & mask) | (code >> 32 - shift)       
        code += ord(c)
    return code

def hash_all_words(shift):
    words_file = open('words.txt', 'r')
    codes = {}
    for word in words_file:
        code = hash_code(word[ : -1], shift)
        if code not in codes:
            codes[code] = 1
        else:
            codes[code] += 1
    hash_counts = list(codes.values())
    hash_counts.sort(reverse = True)
    return hash_counts

def find_best_shifts(top_shifts, bottom_hashes):
    hash_counts_per_shift = []
    for shift in range(32):
        hash_counts = hash_all_words(shift)
        hash_counts_per_shift.append((hash_counts[ : bottom_hashes], shift))
    hash_counts_per_shift.sort()
    return hash_counts_per_shift[ : top_shifts]

if __name__ == '__main__':
    print('Bottom 4 hashes for shift of 0:')
    print(hash_all_words(0)[ : 4])
    print('\nBest 6 shifts for bottom 4 hashes:')
    best_shifts = find_best_shifts(6, 4)
    for hashes, shift in best_shifts:
        print('{:2d} : {:}'.format(shift, hashes))
        
        
        
            
           

