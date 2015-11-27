# Given 2 words, creates an object which can provide the levenshtein distance
# between both words, the alignments of minimal cost between both words,
# and the display of those alignments.
# The costs for insertion, deletion and substitution are set by default to 1, 1 and 2 ,
# respectively, but can be changed.
#
# Written by Eric Martin for COMP9021


class levenshtein_distance:
    '''Given two words word_1 and word_2, builds a table of distances and backtraces
    for the initial segments of word_1 and word_2, from which the Levenshtein distance
    between both words can be computed, as well as the possible alignments of minimal
    distance between both words.'''
    def __init__(self, word_1, word_2, insertion_cost = 1, deletion_cost = 1, substitution_cost = 2):
        self.word_1 = word_1
        self.word_2 = word_2
        self.word_1_length = len(word_1)
        self.word_2_length = len(word_2)
        self.insertion_cost = insertion_cost
        self.deletion_cost = deletion_cost
        self.substitution_cost = substitution_cost
        self._table = self._get_distances_and_backtraces_table()
        self._backtraces = [[self._table[i][j][1] for j in range(self.word_2_length + 1)] for i in range(self.word_1_length + 1)]
        self.aligned_pairs = self.get_aligned_pairs()
        
    def _get_distances_and_backtraces_table(self):
        N_1 = self.word_1_length + 1
        N_2 = self.word_2_length + 1
        # 'H' is for horizontal, corresponding to a deletion,
        # 'V' is for vertical, corresponding to an insertion, and
        # 'D' for diagonal, corresponding to a substitution
        d = {'H' : 0, 'V' : 0, 'D' : 0}
        # Think of table as a sequence of columns, read from left to right,
        # each column beging read from bottom to top, with word_1 and word_2
        # positioned as follows.
        #
        #  2
        #  _
        #  d
        #  r
        #  o
        #  w
        #  .
        #    . w o r d _ 1
        #
        # Each position in the sequence of columns will record the minimal cost of
        # aligning the corresponding initial segment of word_1
        # with the corresponding initial segment of word_2, and also
        # the last move -- horizontal, vertical, diagonal -- from a neighbouring position
        # -- left, below, of left and below, respectively -- that can yield this minimal cost.
        table = [[[0, []] for j in range(N_2)] for i in range(N_1)]
        # Bottom row: cost of deleting more and more letters from word_1.
        for i in range(1, N_1):
            table[i][0] = [i, ['H']]
        # Leftmost column: cost of insertion more and more letters from word_2.
        for j in range(1, N_2):
            table[0][j] = [j, ['V']]
        # Processing all other rows from bottom to top,
        # and each row from left to right, determine the cost
        # of each possible operation:
        # - deleting current letter (of index i-1) of word_1,
        # - inserting current letter (of index j-1) of word_2,
        # - matching or substituting currents letters of word_1 and word_2.
        for i in range(1, N_1):
            for j in range(1, N_2):
                d['H'] = table[i - 1][j][0] + self.deletion_cost
                d['V'] = table[i][j - 1][0] + self.insertion_cost
                if self.word_1[i - 1] == self.word_2[j - 1]:
                    d['D'] = table[i - 1][j - 1][0]
                else:
                    d['D'] = table[i - 1][j - 1][0] + self.substitution_cost
                # Sorting by cost, keeping track of the associated direction.
                distances_and_directions = sorted([(d[x], x) for x in d])
                # Mininal cost...
                table[i][j][0] = distances_and_directions[0][0]
                # ... and its associated direction...
                table[i][j][1].append(distances_and_directions[0][1])
                # ... together with the second direction if associated cost is the same...
                if distances_and_directions[1][0] == distances_and_directions[0][0]:
                    table[i][j][1].append(distances_and_directions[1][1])
                    # ... together with the third direction if associated cost is the same.
                    if distances_and_directions[2][0] == distances_and_directions[1][0]:
                        table[i][j][1].append(distances_and_directions[2][1])
        return table
    
    # Taking pope and paper as an example,
    # since (po*pe*, p*aper) is one of the best aligned pairs,
    # entwined_aligned_pairs will eventually record it
    # (together with all other alignments of minimal cost) as
    # *reepp*ao*pp: po*pe* and p*aper are processed from right to left and entwined.
    # We start at the top right corner of _backtraces, where we find the last directions
    # taken to get there at minimal cost.
    def _compute_alignments(self, i, j, entwined_aligned_pairs):
        # we have reached the lower left corner, so all possible best alignments have been gathered.
        if i == j == 0:
            return
        deletion_pairs = []
        insertion_pairs = []
        substitution_pairs = []
        for direction in self._backtraces[i][j]:
            # entwined_aligned_pairs is the list of all final segments of the best alignments
            # from where we are now to the top right corner, on our way to the bottom left corner.
            # We extend all the best alignments in all directions possible.
            if direction == 'H':
                deletion_pairs = [pair + self.word_1[i - 1] + '*' for pair in entwined_aligned_pairs]
                self._compute_alignments(i - 1, j, deletion_pairs)
            elif direction == 'V':
                insertion_pairs = [pair + '*' + self.word_2[j - 1] for pair in entwined_aligned_pairs]
                self._compute_alignments(i, j - 1, insertion_pairs)
            else:
                substitution_pairs = [pair + self.word_1[i - 1] + self.word_2[j - 1] for pair in entwined_aligned_pairs]
                self._compute_alignments(i - 1, j - 1, substitution_pairs)
        # When the up to three calls to _compute_alignments() have returned,
        # all possible complete extensions of the final segments of the best alignments
        # we had recorded before those calls, and that we needed to make those calls, have been built.
        # We get rid of these finals segments and replace them by all complete best alignments
        # that are now available. 
        entwined_aligned_pairs.clear()
        entwined_aligned_pairs.extend(deletion_pairs + insertion_pairs + substitution_pairs)
        
    def distance(self):
        '''Returns the Levenshtein distance equal to the minimum number of deletions,
        insertions and substitutions needed to transform the first word into the second word,
        with deletions and insertions incurring a cost of 1, and substitutions incurring a cost of 2.

        >>> levenshtein_distance('', '').distance()
        0

        >>> levenshtein_distance('abcde', '').distance()
        5

        >>> levenshtein_distance('', 'abcde').distance()
        5

        >>> levenshtein_distance('a', 'a').distance()
        0

        >>> levenshtein_distance('a', 'b').distance()
        2
        
        >>> levenshtein_distance('aa', 'a').distance()
        1
        
        >>> levenshtein_distance('paris', 'london').distance()
        11
        
        >>> levenshtein_distance('pope', 'paper').distance()
        3
        
        >>> levenshtein_distance('depart', 'leopard').distance()
        5
        '''
        return self._table[self.word_1_length][self.word_2_length][0]

    def get_aligned_pairs(self):
        '''Returns the list of all possible ways to transform the first word into the second word
        and minimising the Levenshtein distance.
        
        >>> levenshtein_distance('', '').get_aligned_pairs()
        [('', '')]

        >>> levenshtein_distance('abcde', '').get_aligned_pairs()
        [('abcde', '*****')]
        
        >>> levenshtein_distance('', 'abcde').get_aligned_pairs()
        [('*****', 'abcde')]

        >>> levenshtein_distance('a', 'a').get_aligned_pairs()
        [('a', 'a')]

        >>> levenshtein_distance('a', 'b').get_aligned_pairs()
        [('*a', 'b*'), ('a*', '*b'), ('a', 'b')]

        >>> levenshtein_distance('aa', 'a').get_aligned_pairs()
        [('aa', 'a*'), ('aa', '*a')]

        >>> levenshtein_distance('pope', 'paper').get_aligned_pairs()
        [('p*ope*', 'pa*per'), ('po*pe*', 'p*aper'), ('pope*', 'paper')]
        
        >>> len(levenshtein_distance('paris', 'london').get_aligned_pairs())
        3653
        '''
        entwined_aligned_pairs = ['']
        self._compute_alignments(self.word_1_length, self.word_2_length, entwined_aligned_pairs)
        aligned_pairs = []
        for pair in entwined_aligned_pairs:
            n = len(pair) // 2 - 1
            word_1 = ''.join([pair[2 * i] for i in range(n, -1, -1)])
            word_2 = ''.join([pair[2 * i + 1] for i in range(n, -1, -1)])
            aligned_pairs.append((word_1, word_2))
        return aligned_pairs

    def display_all_aligned_pairs(self):
        '''Displays all possible ways to transform the first word into the second word
        and minimising the Levenshtein distance.

        >>> levenshtein_distance('depart', 'leopard').display_all_aligned_pairs()
        *de*par*t
        l*eopard*
        <BLANKLINE>
        d*e*par*t
        *leopard*
        <BLANKLINE>
        de*par*t
        leopard*
        <BLANKLINE>
        *de*part*
        l*eopar*d
        <BLANKLINE>
        d*e*part*
        *leopar*d
        <BLANKLINE>
        de*part*
        leopar*d
        <BLANKLINE>
        *de*part
        l*eopard
        <BLANKLINE>
        d*e*part
        *leopard
        <BLANKLINE>
        de*part
        leopard
        '''
        for pair in self.aligned_pairs[ :-1]:
            print(pair[0], '\n', pair[1], '\n', sep = '')
        print(self.aligned_pairs[-1][0], '\n', self.aligned_pairs[-1][1], sep = '')

    
