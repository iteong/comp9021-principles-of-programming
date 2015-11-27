        First_Element_Pairs = [pair[0] for pair in Sorted_PairsList] # list of the first element of each pair
        Second_Element_Pairs = [pair[1] for pair in Sorted_PairsList] # list of the second element of each pair

        # check whether the first element in first pair is less than that of the rest of the pairs, and check
        # whether the second element in first pair is more than that of the rest of the pairs as well
        if First_Element_Pairs[0] < First_Element_Pairs[1:] and Second_Element_Pairs[0] > Second_Element_Pairs[:1]:
            return True
        else:
            return False


        if self._overlap(Sorted_Pairs):
            print("The input defines overlapping pairs.")
            return
        else:
            Sorted_Pairs = [sorted(pair) for pair in OddPairs] 
            if self._overlap(Sorted_Pairs):
                print("The input defines overlapping pairs.")
                return


    # private function to check whether pairs in a list are overlapping
    def _overlap(self, L):
        Two_Pairs = self._two_pairs(L)         
            
        if self._overlap_two_pairs(self, Two_Pairs):
            print('A')
            return True
        else:
            try:
                print('B')
                Sorted_Pairs.pop(1) # remove second pair from Sorted_Pairs and continue comparing
                self._overlap()
            except:
                pass
            return False


    def _two_pairs(self, L):
        print('C')
        self = [L[pair]] + [L[pair+1]] # [[0, 3], [2, 5]] from [[0, 3], [2, 5], [1, 4]]

    
                    
    def _overlap_two_pairs(self, L):
        # for sorted pairs (a,b),(c,d): overlapping cases are c,a,d,b and a,c,b,d
        if L[1][0] < L[0][0] < L[1][1] < L[0][1] or L[0][0] < L[1][0] < L[0][1] < L[1][1]:
            print('D')
            return True
        else:
            print('E')
            return False
