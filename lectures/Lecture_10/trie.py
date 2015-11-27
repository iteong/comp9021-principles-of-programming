# A particular case of general trees: tries
#
# Written by Eric Martin for COMP9021

from binary_tree import *

class Trie:
    def __init__(self):
        self.is_word = False
        self.extensions = {}

    def add_word(self, word):
        current_trie = self
        for c in word:
            if c not in current_trie.extensions:
                current_trie.extensions[c] = Trie()
            current_trie = current_trie.extensions[c]
        current_trie.is_word = True

    def has_been_recorded(self, word):
        current_trie = self
        for c in word:
            if c not in current_trie.extensions:
                return False
            current_trie = current_trie.extensions[c]
        return current_trie.is_word

if __name__ == '__main__':
    trie = Trie()
    for word in ['he', 'hers', 'has', 'heir', 'one']:
        trie.add_word(word)
    print(trie.has_been_recorded('he'))
    print(trie.has_been_recorded('her'))
    print(trie.has_been_recorded('hers'))
    print(trie.has_been_recorded('one'))
    print(trie.has_been_recorded('two'))
        
                
