# Aims: The purpose of the assignment is to:
# - practice the use of stacks;
# - practice performing careful computations;
# - develop problem solving skills.
#
# Find out about simple, alternating, transit mazes at
# http://www.math.stonybrook.edu/~tony/mazes/index.html
#
# The purpose of the assignment is to find out whether a sequence of numbers
# is a level sequence, and if it is, output some Latex code that can be
# processed by pdflatex to produce a pdf file that depicts a maze determined
# by that level sequence.
#
# For the second task, you will probably find that the information about “the
# level sequence of an s.a.t. maze”, accessible from the url above, is
# particularly useful.
#
# Written by Ivan Teong for COMP9021 Assignment 3
#
# Notes: I was only able to complete the input checks and also draw the vertical lines for Maze 5.
#        My method is ignoring the path of the agent, using a mathematical relationship between
#        the vertical/horizontal walls' coordinates and the sequence of even and odd pairs provided
#        to try and draw the maze walls.
#
#        The mathematical relationship can be seen under the section with comments "formatting pairs for drawing walls".
#        The horizontal walls have a relationship with the vertical walls as well, horizontal lines can be drawn from the
#        top and bottom of the vertical lines' upper and lower coordinates (relating to the formatted pair sequences),
#        and each vertical line will also have a horizontal line that it outputs one coordinate away from it on the x and y-axises.
#
#        I think that I chose the wrong strategy as I did not have enough time to finish this assignment unfortunately.
#        Hope that the comments and business logic can gather me some marks on top of the input checks.
#
#        Regarding the maze, the horizontal and vertical lines below an upside-down triangle placed at the upper
#        part of the maze is the same across all mazes, it is only the vertical and horizontal lines above the
#        upside-down triangle that are affected by the sequence level order. My strategy was trying to print out
#        those vertical and horizontal lines below this triangle that are not affected by the level order, and
#        then try to merge the coordinates of the affected upper parts of the vertical lines with the lower part
#        and then work on the horixontal lines, but it is not to be!



class Maze():
    
    def __init__(self, MazeInput):
        self.MazeList = MazeInput.split()
        for i in list(range(len(self.MazeList))):
            try:
                self.MazeList[i] = int(self.MazeList[i])
            except:
                print("The input should consist of numbers.")
                return
            
        # length of input should range between 4 and 20
        if not len(self.MazeList) >= 4 and len(self.MazeList) <= 20:
            print("The input should consist of between 4 and 20 numbers.")
            return
        
        # input in some order is a sorted list that should be equal to range of the length of the input  
        if not list(range(len(self.MazeList))) == sorted(self.MazeList):
            print("The input should consist of 0, 1, 2... N, in some order.")
            return
         
        # check first and last index for 0 and maximum number respectively                     
        if self.MazeList[0] == 0 and self.MazeList[-1] == max(self.MazeList):
            
            # sum of pairs in list alternating between even and odd numbers is always odd
            for i in list(range(len(self.MazeList) - 1)): # check until 2nd last number because checking pairs
                sum_of_pairs = self.MazeList[i] + self.MazeList[i+1]
                if sum_of_pairs % 2 == 0:
                    print("The input should alternate between even and odd numbers.")
                    return 
        else:
            print("The input should start with 0 and end with the largest number.")
            return
    
        EvenPairs = [(self.MazeList[i],self.MazeList[i+1]) for i in range(0, len(self.MazeList) - 1, 2)]
        OddPairs = [(self.MazeList[i],self.MazeList[i+1]) for i in range(1, len(self.MazeList) - 1, 2)]
        
        

        self.even_list = [sorted(pair) for pair in EvenPairs] # [(0,9),(8,5)] => [[0,9],[5,8]]
        self.odd_list = [sorted(pair) for pair in OddPairs]
        




        # iterate through the even and odd sorted lists and checks the selected pair for comparison with the other pairs in the list, see if
        # its first number is in the numbers between the range of the other pair (i.e. (3,6) is turned into all the numbers between its range
        # such as 3,4,5,6), then check if the second number is in them too, if it is not, then it is out of range and are overlapping pairs
        for pair in self.even_list:

            for pair2 in self.even_list:

                if int(pair[0]) in range(int(pair2[0]),int(pair2[1] + 1)) and int(pair[1]) not in range(int(pair2[0]), int(pair2[1] + 1)):

                    print ("The input defines overlapping pairs.")

                    self.even_list = []

                    return

                if int(pair[1]) in range(int(pair2[0]),int(pair2[1] + 1)) and int(pair[0]) not in range(int(pair2[0]), int(pair2[1] + 1)):

                    print ("The input defines overlapping pairs.")

                    self.even_list = []

                    return
                
        for pair in self.odd_list:

            for pair2 in self.odd_list:

                if int(pair[0]) in range(int(pair2[0]),int(pair2[1] + 1)) and int(pair[1]) not in range(int(pair2[0]), int(pair2[1] + 1)):

                    print ("The input defines overlapping pairs.")

                    self.odd_list = []

                    return

                if int(pair[1]) in range(int(pair2[0]),int(pair2[1] + 1)) and int(pair[0]) not in range(int(pair2[0]), int(pair2[1] + 1)):

                    print ("The input defines overlapping pairs.")

                    self.odd_list = []

                    return


        
        # check where the mid line is on the x-axis using the number of digits in the sequence
        if len(self.MazeList) % 2 == 0: # if even number of digits in the sequence      
            self.mid_line = len(self.MazeList) - 1
        else: # if odd number of digits in the sequence
            self.mid_line = len(self.MazeList) - 2
##        print('Mid Line coordinate on x-axis: {:}'.format(self.mid_line))


        
        # formatting pairs for drawing walls
        for pair in self.even_list:
            pair[0] = pair[0] - 1 # deduct 1 from smaller number in all even pairs

        self.even_list[0][0] = self.even_list[0][0] + 1 # add 1 to smaller number in 1st pair


        for pair in self.odd_list:
            pair[0] = pair[0] - 1 # deduct 1 from smaller number in all odd pairs

        self.odd_list[-1][1] = self.odd_list[-1][1] - 1 # deduct 1 from larger number in last odd pairs
        


        # seeing which level is the vertical line at from mid_line by appending * to count levels
        for pair in self.even_list:
            for pair2 in self.even_list:
                if int(pair[0]) in range(int(pair2[0]),int(pair2[1] + 1)) and int(pair[1]) in range(int(pair2[0]), int(pair2[1] + 1)):
                    pair.append('*')

        for pair in self.odd_list:
            for pair2 in self.odd_list:
                if int(pair[0]) in range(int(pair2[0]),int(pair2[1] + 1)) and int(pair[1]) in range(int(pair2[0]), int(pair2[1] + 1)):
                    pair.append('*')


        # assign level to be counter of the number of * in each pair and assign as append as last value
        for pair in self.even_list:
            self.level = pair.count('*')
            pair.append(self.level)

        for pair in self.odd_list:
            self.level = pair.count('*')
            pair.append(self.level)


        # create dictionary with level as dictionary key
        even_dict = {}
        for pair in self.even_list:
            if pair[-1] in even_dict: # check if key exists
                even_dict[pair[-1]].append([pair[0],pair[1]])
            else: # if key don't exist, assign key with values
                even_dict[pair[-1]] = [[pair[0],pair[1]]]
##        print('Even Pairs by Level: {:})'.format(even_dict))


        odd_dict = {}
        for pair in self.odd_list:
            if pair[-1] in odd_dict: # check if key exists
                odd_dict[pair[-1]].append([pair[0],pair[1]])
            else: # if key don't exist, assign key with values
                odd_dict[pair[-1]] = [[pair[0],pair[1]]]
##        print('Odd Pairs by Level: {:})'.format(odd_dict))


        # sort sublists of levels by first value of each pair             
        self.even_levels = list(even_dict.values())
        for level in self.even_levels:
            level.sort(key=lambda level: level[0])
##        print(self.even_levels, len(self.even_levels))

        self.odd_levels = list(odd_dict.values())
        for level in self.odd_levels:
            level.sort(key=lambda level: level[0])
##        print(self.odd_levels, len(self.odd_levels))       


        # add vertical lines y-coordinates that are continued outside affected area
        
        self.even_levels_plus = self.even_levels
        self.even_levels_plus[1].append([8,10])
        self.even_levels_plus[2].append([7,11])

##        print(self.even_levels_plus)

        self.odd_levels_plus = self.odd_levels

##        print(self.odd_levels_plus)
        

        # merge pairs in sublist of even and odd level lists if continuous range
        self.merged_even = [list(self._merge(i)) for i in self.even_levels_plus]
        self.merged_even = self.merged_even[1:] # remove first sublist (level 1) as it is already accounted for (middle vertical line)
##        print(self.merged_even)

        self.merged_odd = [list(self._merge(i)) for i in self.odd_levels_plus]
        self.merged_odd = self.merged_odd[1:] # remove first sublist (level 1) as it is already accounted for (middle vertical line)
##        print(self.merged_odd)
        
        

    # function to merge pairs in sublist if next pair's first number is current
    # pair's second number (continuous range)
    def _merge(self, times):
        saved = list(times[0])
        for st, en in sorted([sorted(t) for t in times]):
            if st <= saved[1]:
                saved[1] = max(saved[1], en)
            else:
                yield list(saved)
                saved[0] = st
                saved[1] = en
        yield list(saved)




    def generate_latex_code(self, name='Unnamed'):
        file = open(name+'.tex', 'a')
        file.write("\\documentclass[10pt]{article}\n")
        file.write("\\usepackage{tikz}\n")
        file.write("\\pagestyle{empty}\n")
        file.write("\n")
        file.write("\\begin{document}\n")
        file.write("\n")
        file.write("\\vspace*{\\fill}\n")
        file.write("\\begin{center}\n")
        file.write("\\begin{tikzpicture}[scale = 1.5, x = 0.25cm, y = -0.25cm, thick, purple]\n")
        file.write("% Horizontal lines\n")
        
        file.write("% Vertical lines\n")
          
        # writing the vertical walls for the first, middle and last lines
        
        if len(self.MazeList) % 2 == 0: # if even number of digits in sequence
            
            # unaffected vertical lines from leftmost up till before vertical lines affected by sequence's level order from even pairs:
            for i, j in zip(list(range(0, self.mid_line - (len(self.even_levels) - 1))), list(reversed(range(0, self.mid_line*2)))):
                 file.write("\\draw(X, X) -- (X, Y);\n".replace('X', str(i)).replace('Y', str(j)))

            # vertical lines for level order sequence of even pairs:

            # level 2
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line - (len(self.even_levels) - 1))).replace('B', str(self.merged_even[-1][0][0])).replace('C', str(self.merged_even[-1][0][1])))
            # level 3
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line - (len(self.even_levels) - 1))).replace('B', str(self.merged_even[-1][1][0])).replace('C', str(self.merged_even[-1][1][1])))
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line - (len(self.even_levels) - 1) + 1)).replace('B', str(self.merged_even[-2][0][0])).replace('C', str(self.merged_even[-2][0][1])))


            # middle vertical line (right vertical line of entry to maze):
            file.write("\\draw(X, 0) -- (X, Y);\n".replace('X', str(self.mid_line)).replace('Y', str(self.mid_line-1)))


            # vertical lines for level order sequence of odd pairs:

            # level 2
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line + (len(self.odd_levels) - 1) - 1)).replace('B', str(self.merged_odd[0][0][0])).replace('C', str(self.merged_odd[0][0][1])))
            # level 3
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line + (len(self.odd_levels) - 1))).replace('B', str(self.merged_odd[1][0][0])).replace('C', str(self.merged_odd[1][0][1])))



            # unaffected vertical lines till rightmost line (after middle and vertical lines affected by sequence's level order from odd pairs):
            for i, j, k in zip(list(range(self.mid_line + (len(self.odd_levels) - 1), self.mid_line*2 + 1)), list(range(self.mid_line, self.mid_line*2)), list(reversed(range(0, self.mid_line)))): 
                 file.write("\\draw(X, Z) -- (X, Y);\n".replace('X', str(i)).replace('Y', str(j)).replace('Z', str(k)))


        else: # if odd number of digits in sequence
            
            # unaffected vertical lines from leftmost up till before vertical lines affected by sequence's level order from even pairs:
            for i, j in zip(list(range(0, self.mid_line - (len(self.even_levels) - 1))), list(reversed(range(0, self.mid_line*2 + 1)))):
                 file.write("\\draw(X, X) -- (X, Y);\n".replace('X', str(i)).replace('Y', str(j)))

            # vertical lines for level order sequence of even pairs:

            # level 2
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line - (len(self.even_levels) - 1))).replace('B', str(self.merged_even[-1][0][0])).replace('C', str(self.merged_even[-1][0][1])))
            # level 3
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line - (len(self.even_levels) - 1))).replace('B', str(self.merged_even[-1][1][0])).replace('C', str(self.merged_even[-1][1][1])))
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line - (len(self.even_levels) - 1) + 1)).replace('B', str(self.merged_even[-2][0][0])).replace('C', str(self.merged_even[-2][0][1])))


            # middle vertical line (right vertical line of entry to maze):

            file.write("\\draw(X, 0) -- (X, Y);\n".replace('X', str(self.mid_line)).replace('Y', str(self.mid_line)))


            # vertical lines for level order sequence of odd pairs:

            # level 2
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line + (len(self.odd_levels) - 1) - 1)).replace('B', str(self.merged_odd[0][0][0])).replace('C', str(self.merged_odd[0][0][1])))
            # level 3
            file.write("\\draw(A, B) -- (A, C);\n".replace('A', str(self.mid_line + (len(self.odd_levels) - 1))).replace('B', str(self.merged_odd[1][0][0])).replace('C', str(self.merged_odd[1][0][1])))


            
            # unaffected vertical lines till rightmost line (after middle and vertical lines affected by sequence's level order from odd pairs):
            for i, j, k in zip(list(range(self.mid_line + (len(self.odd_levels) - 1), self.mid_line*2 + 2)), list(range(self.mid_line + 1, self.mid_line*2 + 1)), list(reversed(range(0, self.mid_line)))): 
                 file.write("\\draw(X, Z) -- (X, Y);\n".replace('X', str(i)).replace('Y', str(j)).replace('Z', str(k)))


        
        file.write("\\end{tikzpicture}\n")
        file.write("\\end{center}\n")
        file.write("\\vspace*{\\fill}\n")
        file.write("\n")
        file.write("\\end{document}\n")
        file.close()
    














    


        
        
