from random import randrange

def display_grid(grid):
    for i in range(8):
        for j in range(8):
            print(grid[i][j], end = '')
        print()


def determine_next_generation(grid, new_grid):
   for i in range(8):
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

def populate_initial_grid(grid, density):
    for i in range(8):
        for j in range(8):
            k = randrange(density)
            if k == 0:
                grid[i][j] = 1

grid = [[[0]* 8 for i in range(8)] for j in range(2)]
populate_initial_grid(grid[0], 4)
    display_grid(grid[0])

switch = True  # 1
for n in range(100):
    determine_next_generation(grid[switch], grid[not switch]) # not switch : 1 - switch
    display_grid(grid[not switch])
    switch = not switch


grid = [[0] * 8 for i in range(8)]
populate_initial_grid(grid, 4)
display_grid(grid)
new_grid = [[None] * 8 for i in range(8)]
print()
determine_next_generation(grid, new_grid)
display_grid(new_grid)
