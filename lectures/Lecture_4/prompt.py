Python 3.4.3 (v3.4.3:9b73f1c3e601, Feb 23 2015, 02:52:03) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "copyright", "credits" or "license()" for more information.
>>> grid = [[0] * 8] * 8
>>> grid
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
>>> grid[0]
[0, 0, 0, 0, 0, 0, 0, 0]
>>> grid[1]
[0, 0, 0, 0, 0, 0, 0, 0]
>>> grid[0][0]
0
>>> def display_grid():
	for i in range(8):
		for j in range(8):
			print(grid[i][j], end = '')

>>> display_grid()
0000000000000000000000000000000000000000000000000000000000000000
>>> def display_grid():
	for i in range(8):
		for j in range(8):
			print(grid[i][j], end = '')
		print()

		
>>> display_grid()
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
>>> def display_grid():
	for i in range(8):
		for j in range(8):
			print(grid[i][j], end = ' ')
		print()

		
>>> display_grid()
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
>>> for i in range(8):
	for j in range(8):
		grid[i][j] = randrange(2)

		
Traceback (most recent call last):
  File "<pyshell#21>", line 3, in <module>
    grid[i][j] = randrange(2)
NameError: name 'randrange' is not defined
>>> from random import randrange
>>> for i in range(8):
	for j in range(8):
		grid[i][j] = randrange(2)

		
>>> display_grid()
0 1 1 0 0 1 1 0 
0 1 1 0 0 1 1 0 
0 1 1 0 0 1 1 0 
0 1 1 0 0 1 1 0 
0 1 1 0 0 1 1 0 
0 1 1 0 0 1 1 0 
0 1 1 0 0 1 1 0 
0 1 1 0 0 1 1 0 
>>> grid = [[0] * 8 for i in range(8)]
>>> display_grid()
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
>>> for i in range(8):
	for j in range(8):
		grid[i][j] = randrange(2)

		
>>> display_grid()
0 0 1 1 0 1 0 0 
1 1 0 1 0 0 1 1 
1 1 0 0 0 0 1 0 
0 1 1 1 1 0 0 1 
1 1 1 0 1 1 0 1 
1 1 1 1 0 0 0 1 
0 0 0 1 1 0 1 0 
0 1 0 0 0 0 0 0 
>>> density = 4
>>> for i in range(8):
	for j in range(8):
		k = randrange(4)
		if k == 0:
			grid[i][j] = 1

			
>>> 
>>> display_grid()
0 1 1 1 1 1 1 0 
1 1 0 1 0 0 1 1 
1 1 0 1 1 0 1 0 
1 1 1 1 1 0 0 1 
1 1 1 0 1 1 0 1 
1 1 1 1 0 0 1 1 
0 0 0 1 1 0 1 1 
1 1 0 0 0 0 0 0 
>>> for i in range(8):
	for j in range(8):
		k = randrange(4)
		if k == 0:
			grid[i][j] = 1

			
>>> display_grid()
0 1 1 1 1 1 1 1 
1 1 0 1 0 0 1 1 
1 1 1 1 1 0 1 0 
1 1 1 1 1 0 0 1 
1 1 1 0 1 1 0 1 
1 1 1 1 0 1 1 1 
1 0 0 1 1 0 1 1 
1 1 0 0 1 0 1 0 
>>> for i in range(8):
	for j in range(8):
		k = randrange(4)
		if k == 0:
			grid[i][j] = 1
		else:
			grid[i][j] = 0

			
>>> display_grid()
0 0 0 1 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 1 0 0 1 0 
0 0 0 1 0 0 0 0 
0 0 0 0 0 0 0 0 
0 1 0 0 0 0 1 0 
0 0 0 0 1 0 0 0 
0 1 0 0 1 0 0 0 
>>> randrange(3)
1
>>> randrange(3)
2
>>> randrange(3)
2
>>> randrange(3)
0
>>> randrange(3)
1
>>> randrange(3)
1
>>> randrange(3)
1
>>> randrange(3)
0
>>> randrange(3)
1
>>> randrange(3)
1
>>> randrange(3)
2
>>> 0 1 0 0 1 0 0 0
SyntaxError: invalid syntax
>>> new_grid = [[None] * 8 for i in range(8)]
>>> for i in range(8):
	for j in range(8):
		nb_of_neighbours = 0
		if i and j and grid[i-1][j-1] == 1:
			nb_of_neighbours += 1
		if i and grid[i-1][j] == 1:
			nb_of_neighbours += 1
		if i and j < 7 and grid[i-1][j+1] == 1:
			nb_of_neighbours += 1
		if j and grid[i][j-1] == 1:
			nb_of_neighbours += 1
		if j < 7 and grid[i][j+1] == 1:
			nb_of_neighbours += 1
		if i < 7 and j and grid[i+1][j-1] == 1:
			nb_of_neighbours += 1
		if i < 7 and grid[i+1][j] == 1:
			nb_of_neighbours += 1
		if i < 7 and j < 7 and grid[i+1][j+1] == 1:
			nb_of_neighbours += 1
		if grid[i][j] == 1  and 2 <= nb_of_neighbours <= 3:
			new_grid[i][j] = 1
		elif grid[i][j] == 0 and nb_of_neighbours == 3:
			new_grid[i][j] = 1
		else:
			new_grid[i][j] = 0

			
>>> display_grid(new_grid)
Traceback (most recent call last):
  File "<pyshell#73>", line 1, in <module>
    display_grid(new_grid)
TypeError: display_grid() takes 0 positional arguments but 1 was given
>>> original_grid = grid
>>> grid = new_grid
>>> display_grid()
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 1 0 0 
0 0 0 0 0 0 0 0 
>>> ======================================================================== RESTART ========================================================================
>>> 
>>> ======================================================================== RESTART ========================================================================
>>> 
Traceback (most recent call last):
  File "/Users/emartin/Desktop/game_of_life.py", line 43, in <module>
    populate_initial_grid(grid, 4)
  File "/Users/emartin/Desktop/game_of_life.py", line 38, in populate_initial_grid
    k = randrange(density)
NameError: name 'randrange' is not defined
>>> ======================================================================== RESTART ========================================================================
>>> 
11000001
10010000
00100000
11010000
11100000
01000011
00000000
01001000
11000000
10100000
10110000
10010000
00000000
11100000
00000000
00000000
>>> ======================================================================== RESTART ========================================================================
>>> 
10000000
00010100
00010001
10000100
01001000
00000000
00010010
00001100

00000000
00001000
00000010
00001000
00000000
00000000
00001100
00001100
>>> grid[[[0]* 8 for i in range(8)] for j in range(2)]
SyntaxError: invalid syntax
>>> grid[[0]* 8 for i in range(8) for j in range(2)]
SyntaxError: invalid syntax
>>> grid = [[[0]* 8 for i in range(8)] for j in range(2)]
>>> grid
[[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]]
>>> grid[0]
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
>>> grid[1]
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
>>> grid[0][i]
Traceback (most recent call last):
  File "<pyshell#83>", line 1, in <module>
    grid[0][i]
NameError: name 'i' is not defined
>>> grid[0][0]
[0, 0, 0, 0, 0, 0, 0, 0]
>>> grid[0][0][0]
0
>>> grid[0]
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
>>> grid[0]
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
>>> grid[1]
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
>>> 
