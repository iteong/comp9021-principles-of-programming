>>> maze = Maze('0 1 2 3 4 A')
The input should consist of numbers.

>>> maze = Maze('0 1 2 3 4 /')
The input should consist of numbers.

>>> maze = Maze('0 1 2')
The input should consist of between 4 and 20 numbers.

>>> maze = Maze('0 1 2 3 5')
The input should consist of 0, 1, 2... N, in some order.

>>> maze = Maze('1 0 2 3 4')
The input should start with 0 and end with the largest number.

>>> maze = Maze('0 1 2 4 3 5')
The input should alternate between even and odd numbers.

>>> maze = Maze('0 3 2 5 4 1 6')
The input defines overlapping pairs.

>>> maze = Maze('0 7 2 1 8 3 4 5 6 9')
The input defines overlapping pairs.

# Copy this to the bottom of your Python file (and delete it before submission).

if __name__ == '__main__':
    print("maze = Maze('0 1 2 3 4 A')")
    maze = Maze('0 1 2 3 4 A')
    print("maze = Maze('0 1 2')")
    maze = Maze('0 1 2')
    print("maze = Maze('0 1 2 3 5')")
    maze = Maze('0 1 2 3 5')
    print("maze = Maze('1 0 2 3 4')")
    maze = Maze('1 0 2 3 4')
    print("maze = Maze('0 1 2 4 3 5')")
    maze = Maze('0 1 2 4 3 5')
    print("maze = Maze('0 3 2 5 4 1 6')")
    maze = Maze('0 3 2 5 4 1 6')
    
    maze = Maze('0 1 2 3')
    maze.generate_latex_code('maze_1_test')

    maze = Maze('0 3 2 1 4')
    maze.generate_latex_code('maze_2_test')

    maze = Maze('0 5 4 1 2 3 6')
    maze.generate_latex_code('maze_3_test')

    maze = Maze('0 7 6 5 4 3 2 1 8')
    maze.generate_latex_code('maze_4_test')

    maze = Maze('0 9 8 5 6 7 4 1 2 3 10')
    maze.generate_latex_code('maze_5_test')

    maze = Maze('0 7 6 5 4 1 2 3 8 11 10 9 12 13 14')
    maze.generate_latex_code('maze_6_test')

    maze = Maze('0 1 2 3 4 5 6 7 8 9 14 13 12 11 10 15')
    maze.generate_latex_code('maze_7_test')
    
    maze = Maze('0 1 2 3 4 5 6 7 8 9 10 11 12 13 14')
    maze.generate_latex_code('maze_8_test')