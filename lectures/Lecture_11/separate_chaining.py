# Separate chaining of compressed hash_codes
#

from cyclic_shift_hash import hash_code

class HashTable:
    def __init__(self, capacity =  65537):
        self._capacity = capacity
        self._table = [None] * capacity
        self._size = 0
        self._cycle = 6

    def _compressed_hash_code(self, word):
        return hash_code(word, self._cycle) % self._capacity

    def add_word(self, word):
        code = self._compressed_hash_code(word)
        if self._table[code] == None:
            self._table[code] = [word]
        else:
            self._table[code].append(word)

    def find_word(self, word):
        code = self._compressed_hash_code(word)
        if not self._table[code] or word not in self._table[code]:
            return False
        return True

    def delete_word(self, word):
        code = self._compressed_hash_code(word)
        if not self._table[code]:
            return False
        words = self._table[code]
        for i in range(len(words)):
            if word == words[i]:
                del words[i]
                return True
        return False

if __name__ == '__main__':
    hash_table = HashTable()
    total_nb_of_words = 0
    words_file = open('words.txt', 'r')
    for word in words_file:
        hash_table.add_word(word[ : -1])
        total_nb_of_words += 1
    nb_of_compressed_hash_codes = 0
    bucket_sizes = []
    for i in range(hash_table._capacity):
        if hash_table._table[i]:
            nb_of_words = len(hash_table._table[i])
            bucket_sizes.append(nb_of_words)
            nb_of_compressed_hash_codes += 1
    print('Nb of words: ', total_nb_of_words)
    print('Nb of compressed hash codes: ', nb_of_compressed_hash_codes)
    bucket_sizes.sort(reverse = True)
    print('Sizes of top 10 fullest buckets:')
    print(bucket_sizes[ : 10])
    print('Trying to find house and ahahahahaha, deleting them, trying to find them again:')
    print(hash_table.find_word('house'))
    print(hash_table.find_word('ahahahahaha'))
    hash_table.delete_word('house')
    hash_table.delete_word('ahahahahaha')
    print(hash_table.find_word('house'))
    print(hash_table.find_word('ahahahahaha'))   
