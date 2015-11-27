from tkinter import *
import tkinter.messagebox
from functools import reduce


DIM = 9
GAP = 30
PEG_COLOUR = '#A0522D'
SELECTION_COLOUR = '#00FFFF'
BOARD_COLOUR = '#DCDCDC'
DELAY = 1000


class Solitaire(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Solitaire')
        menubar = Menu()
        help_menu = Menu(menubar)
        menubar.add_cascade(label = 'Solitaire Help', menu = help_menu)
        help_menu.add_command(label = 'Rules of the game', command = self.rules_help)
        help_menu.add_command(label = 'Defined problems', command = self.defined_problems_help)
        help_menu.add_command(label = 'Reaction to clicks', command = self.reaction_to_clicks_help)
        self.config(menu = menubar)

        buttons = Frame(bd = 20)        
        self.defined_problems_button = Menubutton(buttons, text = 'Defined problems', state = DISABLED)
        self.defined_problems_button.pack(padx = 30, side = LEFT)
        problems = Menu(self.defined_problems_button)
        problems.add_command(label = 'Six marble cross', command = lambda p = 0: self.select_problem(p))
        problems.add_command(label = 'Nine marble cross', command = lambda p = 1: self.select_problem(p))
        problems.add_command(label = 'Triangle', command = lambda p = 2: self.select_problem(p))
        problems.add_command(label = 'Fireplace', command = lambda p = 3: self.select_problem(p))
        problems.add_command(label = 'Calvary', command = lambda p = 4: self.select_problem(p))
        problems.add_command(label = 'Pyramid', command = lambda p = 5: self.select_problem(p))
        problems.add_command(label = 'Double cross', command = lambda p = 6: self.select_problem(p))
        problems.add_command(label = 'Interlaced five crosses', command = lambda p = 7: self.select_problem(p))
        problems.add_command(label = 'Pentagon', command = lambda p = 8: self.select_problem(p))
        problems.add_command(label = 'Inclined square', command = lambda p = 9: self.select_problem(p))
        problems.add_command(label = 'Octogon', command = lambda p = 10: self.select_problem(p))
        problems.add_command(label = 'Triple cross', command = lambda p = 11: self.select_problem(p))
        self.defined_problems_button.config(menu = problems)
        self.select_or_create_problem_button = Button(buttons, text = 'Select defined problem', width = 16, command = self.select_or_create_problem)
        self.select_or_create_problem_button.pack(padx = 30, side = LEFT)               
        self.prepare_to_play_or_play_button = Button(buttons, text = 'Start playing', command = self.prepare_to_play_or_play)
        self.prepare_to_play_or_play_button.pack(padx = 30, side = LEFT)
        self.clear_or_demonstrate_button = Button(buttons, width = 16, text = 'Clear', command = self.clear_or_demonstrate)
        self.clear_or_demonstrate_button.pack(padx = 30)
        buttons.pack()
        self.board = Board()        
        self.board.pack()
        self.selecting_problem = False
        self.selected_problem = None
        self.playing = False
        self.demonstrating = False
        self.demonstrating_further = False

    def rules_help(self):
        tkinter.messagebox.showinfo('Rules of the game',
            'A peg can jump over another peg, "take it" (so the "taken" peg is removed) '
            'and fill a hole, moving either horizontall or vertically.\n\n'
            'The aim is that only one peg be left.')

    def defined_problems_help(self):
        tkinter.messagebox.showinfo('Defined problems',
            'Twelve defined problems are provided.\n\n'
            'When "Select defined problem" is visible on a button, that button can be clicked to allow one of '
            'those problems to be selected from the "Defined problems" dropdown menu. There are then two options:\n'
            ' - Click on the button that displays "Demonstrate solution". This will start the animation '
            'of a solution that can be paused and resumed at will by clicking on the rightmost button, '
            'and which will have to eventually be stopped by clicking on the button that displays "Stop demonstration" '
            'as it starts from the initial configuration again after only one peg is left and the game is over.\n'
            ' - Click on the button that displays "Create own problem" to try and solve the problem manually, '
            'possibly after having modified it, or by setting a new problem by first clicking on the button '
            'which displays "Clear".')

    def reaction_to_clicks_help(self):
        tkinter.messagebox.showinfo('Reaction to clicks',
            'Clicking has not effect:\n'
            ' - after the button that displays "Select defined problem" has been clicked;\n'
            ' - after one the defined problems has been selected;\n'
            ' - after the button that displays "Demonstrate solution" has been clicked '
            'and for as long as the button that displays "Stop demonstration" will not have been clicked.\n\n'
            'If the third button displays "Start playing", then clicking on the board '
            'allows one to insert a new peg (when clicking on a hole) or remove an existing peg.\n\n'
            'If the third button displays "Stop playing", then clicking on the board allows one to:\n'
            ' - select a peg if none is being selected;\n'
            ' - unselect the selected peg, if any;\n'
            ' - jump over and take an adjacent peg by clicking on the hole where the selected peg '
            'will end up, if that move is possible.')

    def select_or_create_problem(self):
        if self.demonstrating or self.selecting_problem:
            self.selecting_problem = False
            self.selected_problem = None
            self.board.selected_problem = None
            self.defined_problems_button.config(state = DISABLED)
            self.select_or_create_problem_button.config(text = 'Select defined problem')
            self.prepare_to_play_or_play_button.config(state = NORMAL)
            self.clear_or_demonstrate_button.config(text = 'Clear', state = NORMAL)
        else:
            self.selecting_problem = True
            self.board.selected_problem = True
            self.defined_problems_button.config(state = NORMAL)
            self.select_or_create_problem_button.config(text = 'Create own problem')
            self.prepare_to_play_or_play_button.config(state = DISABLED)
            self.clear_or_demonstrate_button.config(state = DISABLED)
        if self.demonstrating:
            self.demonstrating = False
            self.demonstrating_further = False
            self.board.selected_problem = None
            self.board.selected_solution = None

    def select_problem(self, p):
        self.selected_problem = p
        self.board.selected_problem = p
        self.board.represent_problem(p)
        self.clear_or_demonstrate_button.config(text = 'Demonstrate solution', state = NORMAL)

    def prepare_to_play_or_play(self):
        self.defined_problems_button.config(state = DISABLED)
        self.select_or_create_problem_button.config(state = DISABLED)
        self.clear_or_demonstrate_button.config(text = 'Clear')
        if self.playing:
            self.playing = False
            self.board.playing = False
            self.select_or_create_problem_button.config(state = NORMAL)
            self.prepare_to_play_or_play_button.config(text = 'Start playing')
            self.clear_or_demonstrate_button.config(state = NORMAL)
            self.board.configuration.positions = self.initial_configuration
            self.board.selected_peg = None
            self.board.represent_configuration()
        else:                
            self.playing = True
            self.board.playing = True
            self.initial_configuration = dict(self.board.configuration.positions)
            self.select_or_create_problem_button.config(state = DISABLED)
            self.prepare_to_play_or_play_button.config(text = 'Stop playing')
            self.clear_or_demonstrate_button.config(state = DISABLED)

    def clear_or_demonstrate(self):
        if self.selected_problem != None:
            if self.demonstrating:
                self.demonstrating_further = not self.demonstrating_further
                self.board.demonstrating_further = self.demonstrating_further
                if self.demonstrating_further:
                    self.clear_or_demonstrate_button.config(text = 'Pause demonstration')
                    self.board.demonstrate()
                else:
                    self.clear_or_demonstrate_button.config(text = 'Resume demonstration')
            else:
                self.demonstrating = True
                self.demonstrating_further = True
                self.board.demonstrating_further = True
                self.board.configuration.selected_solution = list(self.board.configuration.problem_solutions[self.selected_problem])
                self.board.configuration.selected_solution.reverse()
                self.defined_problems_button.config(state = DISABLED)
                self.select_or_create_problem_button.config(text = 'Stop demonstration')
                self.clear_or_demonstrate_button.config(text = 'Pause demonstration')
                self.board.demonstrate()
        else:
            self.board.clear_board()


# We represent the board using the following coding:
#       37 47 57
#    26 36 46 56 66
# 15 25 35 45 55 65 75
# 14 24 34 44 54 64 74
# 13 23 33 43 53 63 73
#    22 32 42 52 62
#       31 41 51
class Configuration:
    def __init__(self):
        locations = reduce(lambda x, y: x + y,
                           map(list, [range(37, 58, 10), range(26, 67, 10),
                                      range(15, 76, 10), range(14, 75, 10), range(13, 74, 10),
                                      range(22, 63, 10), range(31, 52, 10)]))
        self.positions = dict.fromkeys(locations, False)
        self.problems = [[35, 43, 44, 45, 46, 55],
                         [24, 34, 42, 43, 44, 45, 46, 54, 64],
                         [23, 33, 34, 43, 44, 45, 53, 54, 63],
                         [34, 35, 36, 37, 45, 46, 47, 54, 55, 56, 57],
                         [25, 31, 32, 35, 41, 42, 43, 44, 45, 46, 47, 51, 52, 55, 65],
                         [14, 24, 25, 34, 35, 36, 44, 45, 46, 47, 54, 55, 56, 64, 65, 74],
                         [14, 22, 24, 26, 33, 34, 35, 41, 42, 43, 44, 45, 46, 47, 53, 54, 55, 62, 64, 66, 74],
                         [14, 23, 24, 25, 32, 34, 36, 41, 42, 43, 44, 45, 46, 47, 52, 54, 56, 63, 64, 65, 74],
                         [14, 23, 24, 25, 32, 33, 34, 35, 36, 42, 43, 44, 45, 46, 47, 52, 53, 54, 55, 56, 63, 64, 65, 74],
                         [14, 23, 24, 25, 32, 33, 34, 35, 36, 41, 42, 43, 45, 46, 47, 52, 53, 54, 55, 56, 63, 64, 65, 74],
                         list(set(self.positions) - set([13, 15, 31, 37, 51, 57, 73, 75])),
                         list(set(self.positions) - set([22, 26, 44, 62, 66]))]
        self.problem_solutions = [[[45, 65], [43, 45], [35, 55], [65, 45], [46, 44]],
                                  [[43, 41], [45, 43], [24, 44], [44, 42], [64, 44], [41, 43], [43, 45], [46, 44]],
                                  [[53, 55], [55, 35], [33, 53], [63, 43], [44, 42], [35, 33], [23, 43], [42, 44]],
                                  [[45, 25], [37, 35], [57, 37], [34, 36], [37, 35], [25, 45], [46, 66], [54, 56], [66, 46], [46, 44]],
                                  [[31, 33], [51, 53], [43, 63], [41, 43], [33, 53], [63, 43], [44, 42], [46, 44], [25, 45], [45, 43],
                                   [65, 45], [42, 44], [44, 46], [47, 45]],
                                  [[55, 53], [74, 54], [53, 55], [55, 57], [57, 37], [35, 33], [14, 34], [33, 35], [36, 56], [44, 46],
                                   [56, 36], [25, 45], [37, 35], [35, 55], [65, 45]],
                                  [[54, 52], [52, 32], [22, 42], [33, 53], [41, 43], [43, 63], [74, 54], [62, 64], [45, 65], [54, 74],
                                   [66, 64], [74, 54], [35, 33], [54, 34], [33, 35], [47, 45], [45, 25], [14, 34], [26, 24], [24, 44]],
                                  [[64, 62], [44, 64], [74, 54], [46, 66], [66, 64], [64, 44], [44, 46], [47, 45], [24, 26], [26, 46],
                                   [46, 44], [44, 24], [14, 34], [42, 22], [22, 24], [24, 44], [44, 42], [41, 43], [62, 42], [42, 44]],
                                  [[53, 51], [32, 52], [51, 53], [44, 42], [23, 43], [42, 44], [63, 43], [25, 23], [45, 25], [43, 45],
                                   [55, 35], [35, 33], [33, 13], [13, 15], [15, 35], [35, 37], [37, 57], [57, 55], [55, 53], [74, 54],
                                   [53, 55], [65, 45], [46, 44]],
                                  [[53, 51], [51, 31], [55, 75], [75, 73], [73, 53], [64, 44], [35, 37], [37, 57], [57, 55], [55, 35],
                                   [34, 36], [46, 26], [14, 34], [26, 24], [23, 25], [44, 24], [25, 23], [32, 34], [53, 33], [34, 32],
                                   [31, 33], [23, 43], [42, 44]],
                                  [[53, 51], [32, 52], [51, 53], [54, 52], [74, 54], [44, 42], [52, 32], [22, 42], [41, 43], [24, 22],
                                   [43, 23], [22, 24], [62, 64], [64, 44], [34, 54], [14, 34], [66, 64], [64, 44], [56, 54], [35, 33],
                                   [54, 34], [33, 35], [35, 55], [47, 45], [55, 35], [25, 45], [26, 46], [46, 44]],
                                  [[42, 62], [54, 52], [51, 53], [74, 54], [54, 52], [62, 42], [73, 53], [32, 52], [31, 51], [43, 63],
                                   [51, 53], [63, 43], [56, 54], [75, 55], [54, 56], [35, 55], [47, 45], [45, 65], [57, 55], [65, 45],
                                   [37, 35], [34, 32], [13, 33], [15, 13], [43, 23], [13, 33], [32, 34], [24, 26], [34, 36], [26, 46],
                                   [46, 44]]]

    
class Board(Frame):
    def __init__(self):
        Frame.__init__(self, pady = 40)
        self.configuration = Configuration()
        self.drawn_configuration = dict(self.configuration.positions)
        self.board = Canvas(self, width = DIM * GAP, height = DIM * GAP)
        self.board.bind('<1>', self.act_on_click)
        self.draw_board()
        self.board.pack()
        self.selected_problem = None
        self.selected_solution = None
        self.playing = False
        self.selected_peg = None
        self.demonstrating_further = False
        
    def draw_board(self):
        self.board.create_polygon(3 * GAP, 2 * GAP - 5,
                                  5 * GAP + 10, 2 * GAP - 5,
                                  7 * GAP + 15, 4 * GAP,
                                  7 * GAP + 15, 6 * GAP + 10,
                                  5 * GAP + 10, 8 * GAP + 15,
                                  3 * GAP, 8 * GAP + 15,
                                  GAP - 5, 6 * GAP + 10,
                                  GAP - 5, 4 * GAP, fill = BOARD_COLOUR, outline = 'black', width = 2)
        for p in self.configuration.positions:
            x = p // 10 * GAP
            y = (DIM - p) % 10 * GAP
            self.drawn_configuration[p] = self.board.create_oval(x + 1, y + 1, x + 9, y + 9, fill = 'white', outline = 'white')

    def represent_configuration(self):
        for p in self.configuration.positions:
            if self.configuration.positions[p]:
                self.board.itemconfig(self.drawn_configuration[p], fill = PEG_COLOUR, outline = PEG_COLOUR)
                self.configuration.positions[p] = True
            else:
                self.board.itemconfig(self.drawn_configuration[p], fill = 'white', outline = 'white')
                self.configuration.positions[p] = False

    def represent_problem(self, i):
        self.clear_board()
        for p in self.configuration.problems[i]:
            self.board.itemconfig(self.drawn_configuration[p], fill = PEG_COLOUR, outline = PEG_COLOUR)
            self.configuration.positions[p] = True

    def clear_board(self):
        for p in self.drawn_configuration:
            self.board.itemconfig(self.drawn_configuration[p], fill = 'white', outline = 'white')
            self.configuration.positions[p] = False

    def position_where_clicked(self, event):
        x = round(self.board.canvasx(event.x))
        y = round(self.board.canvasx(event.y))
        x_last_digit = x % 10
        y_last_digit = y % 10
        if not (1 <= x_last_digit <= 9 and 1 <= y_last_digit <= 9):
            return None
        x -= x_last_digit
        y -= y_last_digit
        if x % GAP or y % GAP:
            return None
        x //= GAP
        y = DIM - y // GAP
        p = x * 10 + y
        return p

    def act_on_click(self, event):
        if self.selected_problem != None:
            return
        if not self.playing:
            self.insert_or_remove_peg(event)
        else:
            self.select_peg_or_jump_and_take(event)

    def insert_or_remove_peg(self, event):
        p = self.position_where_clicked(event)
        if p:
            if self.configuration.positions[p]:
                self.board.itemconfig(self.drawn_configuration[p], fill = 'white', outline = 'white')
            else:
                 self.board.itemconfig(self.drawn_configuration[p], fill = PEG_COLOUR, outline = PEG_COLOUR)
            self.configuration.positions[p] = not self.configuration.positions[p]

    def select_peg_or_jump_and_take(self, event):
        p = self.position_where_clicked(event)
        if not p:
            return
        x = p // 10
        y = p % 10
        if self.selected_peg:
            if self.selected_peg == p:
                self.board.itemconfig(self.drawn_configuration[p], fill = PEG_COLOUR, outline = PEG_COLOUR)
                self.selected_peg = None
            elif not self.configuration.positions[p]:
                x_diff = self.selected_peg // 10 - x
                y_diff = self.selected_peg % 10 - y
                if (x_diff == 0 or y_diff == 0) and (abs(x_diff) == 2 or abs(y_diff) == 2):
                    self.try_and_take_peg(p, x_diff // 2, y_diff // 2)
        elif self.configuration.positions[p]:
            self.board.itemconfig(self.drawn_configuration[p], fill = SELECTION_COLOUR, outline = SELECTION_COLOUR)
            self.selected_peg = p
                    
    def try_and_take_peg(self, p, x_half_diff, y_half_diff):
        if y_half_diff:
            position_of_peg_to_take = p + y_half_diff
        else:
            position_of_peg_to_take = p + x_half_diff * 10
        if not self.configuration.positions[position_of_peg_to_take]:
            return
        if y_half_diff:
            position_of_taking_peg = p + 2 * y_half_diff
        else:
            position_of_taking_peg = p + 2 * x_half_diff * 10
        self.board.itemconfig(self.drawn_configuration[position_of_taking_peg], fill = 'white', outline = 'white')
        self.configuration.positions[position_of_taking_peg] = False
        self.board.itemconfig(self.drawn_configuration[position_of_peg_to_take], fill = 'white', outline = 'white')
        self.configuration.positions[position_of_peg_to_take] = False
        self.board.itemconfig(self.drawn_configuration[p], fill = PEG_COLOUR, outline = PEG_COLOUR)
        self.configuration.positions[p] = True
        self.selected_peg = False

    def demonstrate(self):
        if self.selected_peg:               
            self.selected_peg = False
            self.board.itemconfig(self.drawn_configuration[self.from_position], fill = 'white', outline = 'white')
            self.configuration.positions[self.from_position] = False
            taken_position = (self.from_position // 10 + self.to_position // 10) // 2 * 10 + (self.from_position % 10 + self.to_position % 10) // 2
            self.board.itemconfig(self.drawn_configuration[taken_position], fill = 'white', outline = 'white')
            self.configuration.positions[taken_position] = False
            self.board.itemconfig(self.drawn_configuration[self.to_position], fill = PEG_COLOUR, outline = PEG_COLOUR)
            self.configuration.positions[self.to_position] = True
            self.after(DELAY, self.demonstrate)
        elif self.selected_problem == None:
            return
        elif self.demonstrating_further:
            if not self.selected_solution:
                self.represent_problem(self.selected_problem)
                self.selected_solution = list(self.configuration.problem_solutions[self.selected_problem])
                self.selected_solution.reverse()
                self.after(DELAY, self.demonstrate)
            else:
                self.from_position, self.to_position = self.selected_solution.pop()
                self.board.itemconfig(self.drawn_configuration[self.from_position], fill = SELECTION_COLOUR, outline = SELECTION_COLOUR)
                self.selected_peg = True
                self.after(DELAY, self.demonstrate)



if __name__ == '__main__':
    Solitaire().mainloop()
