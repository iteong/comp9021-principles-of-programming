## Write a program named solitaire.py.
##
## Written by Ivan Teong for COMP9021
##
## Aims:
##
## The purpose of the assignment is to:
## • design and implement an interface based on the desired behaviour of an application program;
## • practice the use of functions encapsulated in a class and some builtin data structures, lists in particular;
## • develop problem solving skills.
##
## We refer to the positions of the board as follows:
##
##               37 47 57
##            26 36 46 56 66
##         15 25 35 45 55 65 75
##         14 24 34 44 54 64 74
##         13 23 33 43 53 63 73
##            22 32 42 52 62         
##               31 41 51
##

from functools import reduce

class Solitaire:
    def __init__(self):
        self.locations = reduce(lambda x, y: x + y,
                           map(list, [range(37, 58, 10), range(26, 67, 10),
                                      range(15, 76, 10), range(14, 75, 10), range(13, 74, 10),
                                      range(22, 63, 10), range(31, 52, 10)]))
        self.positions = dict.fromkeys(self.locations, False)
        
    def set_configuration(self, arg_list = []):
        self.positions = dict.fromkeys(self.positions, False)
        for key in arg_list:
            if key in self.positions:
                self.positions[key] = True
            else:
                if not arg_list:
                    self.positions = dict.fromkeys(self.positions, False) # change all dict values to False
                    return
                else:
                    print('Invalid configuration.')
                    self.positions = dict.fromkeys(self.positions, False)
                    return

    def get_configuration(self):
        self.get_configuration_list = []
        for value in range(len(self.locations)): # value in list locations which is ordered
            if self.positions[self.locations[value]] == True: # if value in list is value in dict equals True
                self.get_configuration_list.append(self.locations[value]) # append value in list to new_list

        return self.get_configuration_list

    def configuration_is(self, arg_list = []):
        self.configuration_is_list = []
        for value in range(len(self.locations)): # value in list locations which is ordered
            if self.positions[self.locations[value]] == True: # if value in list is value in dict equals True
                self.configuration_is_list.append(self.locations[value])
        
        if all(value in arg_list for value in self.configuration_is_list):
            if len(set(arg_list)) == len(set(self.configuration_is_list)):
                return True
            else:
                return False
        else:
            return False

    def get_configuration_length(self):
        self.configuration_length_list = []
        for value in range(len(self.locations)): # value in list locations which is ordered
            if self.positions[self.locations[value]] == True: # if value in list is value in dict equals True
                self.configuration_length_list.append(self.locations[value])
                
        return int(len(self.configuration_length_list))
        
    def display_configuration(self):
        self.printer = dict(self.positions)     # copies dictionary into new dictionary so changing of values
        for key in self.printer:                # into 'X' and 'O' does not affect original dictionary's 'True'
            if self.printer[key] == True:       # and 'False' values (original dictionary may be called elsewhere)
                self.printer[key] = 'X' 
            elif self.printer[key] == False:
                self.printer[key] = 'O'

        print("    " + " ".join([self.printer[i] for i in range(37, 58, 10)])) # checks dictionary for these keys
        print("  " + " ".join([self.printer[i] for i in range(26, 67, 10)])) # and create a new list [] with the
        print("" + " ".join([self.printer[i] for i in range(15, 76, 10)])) # values of the 3 dictionary keys
        print("" + " ".join([self.printer[i] for i in range(14, 75, 10)]))
        print("" + " ".join([self.printer[i] for i in range(13, 74, 10)]))
        print("  " + " ".join([self.printer[i] for i in range(22, 63, 10)]))
        print("    " + " ".join([self.printer[i] for i in range(31, 52, 10)]))

    def set_complement_configuration(self, arg_list = []):
        for key in self.positions:
            self.positions[key] = True
            if key in arg_list:
                self.positions[key] = False
            elif not arg_list:
                self.positions[key] = True
        
    def apply_jumps(self, arg_list = []):

        if not arg_list: # if input is empty list
            print('Invalid sequence of jumps.')
            return
        
        for item in arg_list: # item = [value1, value2] in bigger list
            # if difference of jump values not 20 or 2 2 
            if abs(item[0] - item[1]) != 20 and abs(item[0] - item[1]) != 2:                
                print('Invalid sequence of jumps.')
                return
            # input has 1 value not in board value
            elif item[0] not in self.locations or item[1] not in self.locations:
                print('Invalid sequence of jumps.')
                return
            # input has both values not in board value
            elif item[0] not in self.locations and item[1] not in self.locations:
                print('Invalid sequence of jumps.')
                return
            
        for item in arg_list: # changing values in dictionary if all inputs valid
            if self.positions[item[0]] == True and self.positions[item[1]] == False and self.positions[(item[0]+item[1])//2] == True:
                
                self.positions[item[0]] = False

                self.positions[(item[0]+item[1])//2] = False

                self.positions[item[1]] = True

            else:
                print('Invalid sequence of jumps.')
                return

    def display_jumps(self, arg_list = []):
        index = 0 # use index to check whether item is last in the list
        for item in arg_list: # item = [value1, value2] in bigger list
            if index != len(arg_list) - 1: # if the item is not last in the list, print new line at every iteration
                if self.positions[item[0]] == True:
                    self.positions[item[0]] = False

                if self.positions[(item[0]+item[1])//2] == True:
                    self.positions[(item[0]+item[1])//2] = False

                if self.positions[item[1]] == False:
                    self.positions[item[1]] = True

                self.display = dict(self.positions)
                for key in self.display:                
                    if self.display[key] == True:       
                        self.display[key] = 'X' 
                    elif self.display[key] == False:
                        self.display[key] = 'O'

                print("    " + " ".join([self.display[i] for i in range(37, 58, 10)]))
                print("  " + " ".join([self.display[i] for i in range(26, 67, 10)]))
                print("" + " ".join([self.display[i] for i in range(15, 76, 10)]))
                print("" + " ".join([self.display[i] for i in range(14, 75, 10)]))
                print("" + " ".join([self.display[i] for i in range(13, 74, 10)]))
                print("  " + " ".join([self.display[i] for i in range(22, 63, 10)]))
                print("    " + " ".join([self.display[i] for i in range(31, 52, 10)]) + '\n')
                index += 1
            else:
                if self.positions[item[0]] == True:
                    self.positions[item[0]] = False

                if self.positions[(item[0]+item[1])//2] == True:
                    self.positions[(item[0]+item[1])//2] = False

                if self.positions[item[1]] == False:
                    self.positions[item[1]] = True

                self.display = dict(self.positions)
                for key in self.display:                
                    if self.display[key] == True:       
                        self.display[key] = 'X' 
                    elif self.display[key] == False:
                        self.display[key] = 'O'

                print("    " + " ".join([self.display[i] for i in range(37, 58, 10)]))
                print("  " + " ".join([self.display[i] for i in range(26, 67, 10)]))
                print("" + " ".join([self.display[i] for i in range(15, 76, 10)]))
                print("" + " ".join([self.display[i] for i in range(14, 75, 10)]))
                print("" + " ".join([self.display[i] for i in range(13, 74, 10)]))
                print("  " + " ".join([self.display[i] for i in range(22, 63, 10)]))
                print("    " + " ".join([self.display[i] for i in range(31, 52, 10)]))
            
    def apply_reverse_jumps(self, arg_list = []):

        copy_of_positions = self.positions.copy()

        arg_list.reverse()
        
        if not arg_list: # if input is empty list
            print('Invalid sequence of jumps.')
            return
        
        for item in arg_list: # item = [value1, value2] in bigger list
            # if difference of jump values not 20 or 2
            if abs(item[0] - item[1]) != 20 and abs(item[0] - item[1]) != 2:                
                print('Invalid sequence of jumps.')
                return
            # input has 1 value not in board value
            elif item[0] not in self.locations or item[1] not in self.locations:
                print('Invalid sequence of jumps.')
                return
            # input has both values not in board value
            elif item[0] not in self.locations and item[1] not in self.locations:
                print('Invalid sequence of jumps.')
                return

        for item in arg_list: # changing values in dictionary if all inputs valid
    
            if copy_of_positions[item[0]] == False and copy_of_positions[item[1]] == True and copy_of_positions[(item[0]+item[1])//2] == False:
                
                copy_of_positions[item[0]] = True

                copy_of_positions[(item[0]+item[1])//2] = True

                copy_of_positions[item[1]] = False

            else:
                print('Invalid sequence of jumps.')
                return
            
        self.positions = copy_of_positions.copy()


    def display_reverse_jumps(self, arg_list = []):

        arg_list.reverse()
        
        index = 0 # use index to check whether item is last in the list
        for item in arg_list: # item = [value1, value2] in bigger list
            if index != len(arg_list) - 1: # if the item is not last in the list, print new line at every iteration
                if self.positions[item[0]] == False:
                    self.positions[item[0]] = True

                if self.positions[(item[0]+item[1])//2] == False:
                    self.positions[(item[0]+item[1])//2] = True

                if self.positions[item[1]] == True:
                    self.positions[item[1]] = False

                self.display = dict(self.positions)
                for key in self.display:                
                    if self.display[key] == True:       
                        self.display[key] = 'X' 
                    elif self.display[key] == False:
                        self.display[key] = 'O'

                print("    " + " ".join([self.display[i] for i in range(37, 58, 10)]))
                print("  " + " ".join([self.display[i] for i in range(26, 67, 10)]))
                print("" + " ".join([self.display[i] for i in range(15, 76, 10)]))
                print("" + " ".join([self.display[i] for i in range(14, 75, 10)]))
                print("" + " ".join([self.display[i] for i in range(13, 74, 10)]))
                print("  " + " ".join([self.display[i] for i in range(22, 63, 10)]))
                print("    " + " ".join([self.display[i] for i in range(31, 52, 10)]) + '\n')
                index += 1
                
            else:
                if self.positions[item[0]] == False:
                    self.positions[item[0]] = True

                if self.positions[(item[0]+item[1])//2] == False:
                    self.positions[(item[0]+item[1])//2] = True

                if self.positions[item[1]] == True:
                    self.positions[item[1]] = False

                self.display = dict(self.positions)
                for key in self.display:                
                    if self.display[key] == True:       
                        self.display[key] = 'X' 
                    elif self.display[key] == False:
                        self.display[key] = 'O'

                print("    " + " ".join([self.display[i] for i in range(37, 58, 10)]))
                print("  " + " ".join([self.display[i] for i in range(26, 67, 10)]))
                print("" + " ".join([self.display[i] for i in range(15, 76, 10)]))
                print("" + " ".join([self.display[i] for i in range(14, 75, 10)]))
                print("" + " ".join([self.display[i] for i in range(13, 74, 10)]))
                print("  " + " ".join([self.display[i] for i in range(22, 63, 10)]))
                print("    " + " ".join([self.display[i] for i in range(31, 52, 10)]))

            
    def list_possible_next_jump(self):
        
        jumps = [] # create new list for printing appended values that are valid jumps
        
        for key in self.locations: # checking for the value in ordered list, self.locations
            
            if self.positions[key] == True: # checking the dictionary value whether it is True

                if self._check_jump(key, key + 2) is True:
                    jumps.append([key, key + 2])

                if self._check_jump(key, key - 20) is True:
                    jumps.append([key, key - 20])

                if self._check_jump(key, key + 20) is True:
                    jumps.append([key, key + 20])

                if self._check_jump(key, key - 2) is True:
                    jumps.append([key, key - 2])
                                       
        return jumps


    def _check_jump(self, start, end):
        
        if end not in self.positions.keys(): # if jump's destination value not in dictionary
            return False
                                       
        else:
            if self.positions[end] == True: # if jump's destination value is True "X" (should be "O")
                return False
            if self.positions[(start+end)//2] == False: # if jump's middle value is False "O" (should be "X")
                return False
            
        return True           


    def generated_sequence_of_jumps(self, goal=None):

        if goal is None:
            
            if not self.list_possible_next_jump: # base case with no possible further jumps
                return longest_jump_sequence

            longest_jump_sequence = [] # find longest_jump_sequence to get least pegs
            
            for i in self.list_possible_next_jump():

                jumps = [i] # create a new list containing i-th possible jump list
                self.apply_jumps([i]) # execute the jump using apply_jumps
                
                longest_jump_sequence = self.generated_sequence_of_jumps() # call recursion

                longest_jump_sequence = jumps + longest_jump_sequence
                
                if len(jumps) > len(longest_jump_sequence):
                    longest_jump_sequence = jumps

                self.apply_reverse_jumps([i])

            return longest_jump_sequence

        else:
            
            longest_jump_sequence = []

            self.a = self.get_configuration()
                
            if self.a == goal: # check whether final configuration equals to that of goal
                return longest_jump_sequence

            else:
                
                for i in self.list_possible_next_jump():
                    
                    jumps = [i]
                    self.apply_jumps([i])

                    longest_jump_sequence = self.generated_sequence_of_jumps()
                        

                    if len(self.get_configuration()) < len(goal): # check if length of final configuration 
                        self.apply_reverse_jumps([i]) # less than that of goal
                        continue # goes to jumps = [i] if this condition is true

                    longest_jump_sequence = jumps + longest_jump_sequence

                    if len(jumps) > len(longest_jump_sequence):
                        longest_jump_sequence = jumps

                    self.apply_reverse_jumps([i])


                return longest_jump_sequence



