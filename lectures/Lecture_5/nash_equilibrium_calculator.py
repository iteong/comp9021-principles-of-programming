# Written by Eric Martin for COMP9021

from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
import re


CELL_COLOUR = '#F5F5F5'
VALUE_COLOUR = '#330033'
RUTH_COLOUR = '#000099'
CHARLIE_COLOUR = '#556B2F'
NASH_COLOUR = '#CC0000'
ERROR_COLOUR = '#FFCCCC'


class NashEquilibriumCalculator(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Nash Equilibrium Calculator')
        menubar = Menu()
        help_menu = Menu(menubar)
        menubar.add_cascade(label = 'Nash Equilibrium Calculator Help', menu = help_menu)
        help_menu.add_command(label = 'Input', command = self.input_help)
        help_menu.add_command(label = 'Output', command = self.output_help)
        help_menu.add_command(label = 'Possible cases', command = self.possible_cases_help)
        self.config(menu = menubar)
        
        self.game_matrix = GameMatrix()
        self.game_matrix.pack()
        self.graph = Canvas(self, width = 140, height = 140)
        self.graph.pack()
        special_expectations_0 = StringVar()
        special_expectations_1 = StringVar()
        Label(self, textvariable = special_expectations_0, width = 65).pack()
        Label(self, textvariable = special_expectations_1, width = 65).pack()
        self.special_expectations = [special_expectations_0, special_expectations_1]
        Button(self, text = 'Compute Nash equilibria', width = 20, pady = 30,
               command = self.display_graphics_and_special_information).pack()

    def input_help(self):
        tkinter.messagebox.showinfo('Input',
            "Ruth's payoffs are the first member of the pair, and Charlie's payoffs the second member.\n\n"
            "Ruth chooses the second column with probability p, and the first one with probability 1 - p. "
            "Charlie chooses the first row with probability q, and the second one with probability 1 - q.\n\n")

    def output_help(self):
        tkinter.messagebox.showinfo('Output',
            "Ruth's regret lines are displayed in blue, and Charlie's in green; "
            "their intersection is displayed in red.\n\n"
            "Pure equilibria are displayed as red circles in corners of the graph "
            "and the corresponding cells are highlighted.\n\n"
            "When Ruth or Charlie uses a mixed strategy and the opponent's expected payoff "
            "does not depend on his or her choice of probability, then Ruth or Charlie's choice of probability "
            "and the opponent's corresponding expected payoff are explicited. "
            "When the information for both is explicited, this corresponds to a nonpure Nash equilibrium, "
            "with the two regret lines intersecting at a position indicated by a red circle.")

    def possible_cases_help(self):
        tkinter.messagebox.showinfo('Possible cases',
            'There are 9 possible cases for Ruth and for Charlie, so a total of 81 possible cases.\n\n'
            'Entered in the order lower left, upper left, lower right, upper right for Ruth '
            'and in the order lower left, lower right, upper left, upper right for Charlie, '
            'the 9 cases can be illustrated with the following values:\n\n'
            '      1 2 2 4\n'
            '      0 -1 0 0\n'
            '      3 2 2 4\n'
            '      1 1 0 1\n'
            '      4 2 2 1\n'
            '      -1 -1 0 -1\n'
            '      2 3 4 -3\n'
            '      0 1 0 0\n'
            '      0 0 0 0')

    def display_graphics_and_special_information(self):
        self.game_matrix.restore_default_colours()
        self.special_expectations[0].set('')
        self.special_expectations[1].set('')
        self.graph.delete(ALL)
        if self.game_matrix.get_payoffs():
            self.analyse_game(self.game_matrix.payoffs)
            self.draw_regret_lines_and_highlight_cells(self.graph, self.segments, self.game_matrix.cells)
            self.display_information_about_special_expectations(self.special_expectations, self.expectations, self.probas)

    def analyse_game(self, payoffs):
        # Let a1, a2, a3 and a4 denote payoff[0][0][0], payoff[0][0][1], payoff[0][1][0] and payoff[0][1][1], respectively.
        # Let b1, b2, b3 and b4 denote payoff[1][0][0], payoff[1][0][1], payoff[1][1][0] and payoff[1][1][1], respectively.
        # Set D[0] = a1  -a2 - a3 + a4 and D[1] = b1 - b2 - b3 + b4.
        # Set E[0] = a3 - a1 and E[1] = b2 - b1.
        # Set F[0] = a2 - a1 and F[1] = b3 - b1.
        #
        # When Ruth selects the second column with probability p and Charlie selects the second row with probability q,
        # Ruths' expectation is equal to (D[0] * q + E[0]) * p + F[0] * q + a1 and
        # Charlie's expectation is equal to (D[1] * p + E[1]) * q + F[1] * p + b1.
        # Both players maximise their expectation, which determines:
        # - Ruth's No Regret graph, consisting of all pairs of numbers of the form:
        #   * (0, q) with D[0] * q + E[0] < 0
        #   * (p, q) with 0 <= p <= 1 and D[0] * q + E[0] == 0
        #   * (1, q) with D[0] * q + E[0] > 0
        # - Charlie's No Regret graph, consisting of all pairs of numbers of the form:
        #   * (p, 0) with D[1] * p + E[1] < 0
        #   * (p, q) with 0 <= q <= 1 and D[1] * p + E[1] == 0
        #   * (q, 1) with D[1] * q + E[1] > 0
        #
        # When there exists a unique q in [0, 1] with D[0] * q + E[0] == 0,
        # then that q is recorded as both probas[0] and segments[0][1];
        # moreover, if q is in (0, 1) then Ruth's corresponding expectation,
        # which does not depend on p and is equal to F[0] * q + a1, is recorded as self.expectations[0].
        # When there exists a unique p in [0, 1] with D[1] * p + E[1] == 0,
        # then that p is recorded as both probas[1] and segments[1][1]
        # moreover, if p is in (0, 1) then Charlie's corresponding expectation,
        # which does not depend on q and is equal to F[1] * p + b1, is recorded as self.expectations[1].
        # When there is a largest q in [0,1] with D[0] * q' + E[0] < 0 for all q' < q,
        # then [0, q] is recorded as segments[0][0].
        # When there is a largest p in [0,1] with D[1] * p' + E[1] < 0 for all p' < p,
        # then [0, p] is recorded as segments[1][0].
        # When there is a smallest q in [0,1] with D[0] * q' + E[0] > 0 for all q' > q,
        # then [q, 1] is recorded as segments[0][2].
        # When there is a smallest p in [0,1] with D[1] * p' + E[1] > 0 for all p' > p,
        # then [p, 1] is recorded as segments[1][2].
        self.segments = [[None, None, None], [None, None, None]]
        self.probas = [None, None]
        self.expectations = [None, None]
        D = [None, None]
        E = [None, None]
        F = [None, None]
        for k in [0, 1]:
            payoff = payoffs[k]
            D[k] = payoff[0][0] - payoff[0][1] - payoff[1][0] + payoff[1][1]
            if k == 0:
                E[k] = payoff[1][0] - payoff[0][0]
            else:
                E[k] = payoff[0][1] - payoff[0][0]                   
            if D[k]:
                self.probas[k] = -E[k] / D[k]
                if self.probas[k] < 0 or self.probas[k] > 1:
                    if E[k] < 0:
                        self.segments[k][0] = [0, 1]
                    else:
                        self.segments[k][2] = [0, 1]
                else:
                    self.segments[k][1] = self.probas[k]
                    if self.probas[k] == 1:
                        if D[k] > 0:
                            self.segments[k][0] = [0, 1]
                            self.segments[k][2] = [1, 1]
                        else:
                            self.segments[k][2] = [0, 1]
                            self.segments[k][0] = [1, 1]
                    elif self.probas[k] == 0:
                        if D[k] > 0:
                            self.segments[k][0] = [0, 0]
                            self.segments[k][2] = [0, 1]
                        else:
                            self.segments[k][2] = [0, 0]
                            self.segments[k][0] = [0, 1]
                    else:
                        if k == 0:
                            F[k] = payoff[0][1] - payoff[0][0]
                        else:
                            F[k] = payoff[1][0] - payoff[0][0]
                        self.expectations[k] = F[k] * self.probas[k] + payoff[0][0]
                        if D[k] > 0:
                            self.segments[k][0] = [0, self.probas[k]]
                            self.segments[k][2] = [self.probas[k], 1]
                        else:
                            self.segments[k][0] = [self.probas[k], 1]
                            self.segments[k][2] = [0, self.probas[k]]
            elif E[k] < 0:
                self.segments[k][0] = [0, 1]
            elif E[k] > 0:
                self.segments[k][2] = [0, 1]

    def draw_regret_lines_and_highlight_cells(self, graph, segments, cells):
        segments_0 = segments[0]
        segments_1 = segments[1]
        graph.create_text(57, 130, text = 'p', fill = RUTH_COLOUR)
        graph.create_text(7, 120, text = '0', fill = RUTH_COLOUR)
        graph.create_text(107, 120, text = '1', fill = RUTH_COLOUR)
        graph.create_text(135, 57, text = 'q', fill = CHARLIE_COLOUR)
        graph.create_text(120, 7, text = '1', fill = CHARLIE_COLOUR)
        graph.create_text(120, 107, text = '0', fill = CHARLIE_COLOUR)
        if not segments_0[0] and segments_0[2]:
            if not segments_1[0] and segments_1[2]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif not segments_1[2] and segments_1[0]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = CHARLIE_COLOUR, outline = CHARLIE_COLOUR)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
        elif segments_0[0] == [0, 0] and segments_0[2] == [0, 1]:
            if not segments_1[0] and segments_1[2]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
                cells[0][0].config(fg = NASH_COLOUR)               
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)                
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif not segments_1[2] and segments_1[0]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)                
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)               
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR) 
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = CHARLIE_COLOUR, outline = CHARLIE_COLOUR)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(0, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
        elif segments_0[1] and segments_0[0][0] == 0 and 0 < segments_0[1] < 1:
            if not segments_1[0] and segments_1[2]:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
                cells[0][0].config(fg = NASH_COLOUR)               
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(segments_1[1] * 100 + 3, (1- segments_0[1]) * 100 + 3, segments_1[1] * 100 + 7,
                                  (1 - segments_0[1]) * 100 + 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)                
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
            elif not segments_1[2] and segments_1[0]:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105,
                                       fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(segments_1[1] * 100 + 3, (1 - segments_0[1]) * 100 + 3, segments_1[1] * 100 + 7,
                                  (1 - segments_0[1]) * 100 + 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5,
                                       fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(6, 6, 105, 105, fill = CHARLIE_COLOUR, outline = CHARLIE_COLOUR)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
        elif segments_0[0] == [0, 1] and segments_0[2] == [1, 1]:
            if not segments_1[0] and segments_1[2]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif not segments_1[2] and segments_1[0]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_line(5, 5, 105, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)               
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = CHARLIE_COLOUR, outline = CHARLIE_COLOUR)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)       
        elif not segments_0[2] and segments_0[0]:
            if not segments_1[0] and segments_1[2]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)                
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
            elif not segments_1[2] and segments_1[0]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)               
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)               
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = CHARLIE_COLOUR, outline = CHARLIE_COLOUR)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
        elif segments_0[0] == [1, 1] and segments_0[2] == [0, 1]:
            if not segments_1[0] and segments_1[2]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_line(5, 5, 105, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif not segments_1[2] and segments_1[0]:
                graph.create_line(5, 5, 105, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)               
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR) 
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)               
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_line(5, 5, 105, 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = CHARLIE_COLOUR, outline = CHARLIE_COLOUR)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
        elif segments_0[1] and segments_0[0][1] == 1 and 0 < segments_0[1] < 1:
            if not segments_1[0] and segments_1[2]:
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(segments_1[1] * 100 + 3, (1 - segments_0[1]) * 100 + 3, segments_1[1] * 100 + 7,
                                  (1 - segments_0[1]) * 100 + 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)               
            elif not segments_1[2] and segments_1[0]:
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, (1 - segments_0[1]) * 100 + 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)               
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(segments_1[1] * 100 + 3, (1 - segments_0[1]) * 100 + 3, segments_1[1] * 100 + 7,
                                  (1 - segments_0[1]) * 100 + 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR) 
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = CHARLIE_COLOUR, outline = CHARLIE_COLOUR)
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
        elif segments_0[0] == [0, 1] and segments_0[2] == [0, 0]:
            if not segments_1[0] and segments_1[2]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)               
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_line(5, 105, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif not segments_1[2] and segments_1[0]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)                
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 5, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, (1 - segments_0[1]) * 100 + 5, 105, (1 - segments_0[1]) * 100 + 5, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(105, (1 - segments_0[1]) * 100 + 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_line(5, 5, 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = RUTH_COLOUR, width = 2)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = CHARLIE_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = CHARLIE_COLOUR, outline = CHARLIE_COLOUR)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
        elif not segments_0[0] and not segments_0[0]:
            if not segments_1[0] and segments_1[2]:
                graph.create_rectangle(5, 5, 105, 105, fill = RUTH_COLOUR, outline = RUTH_COLOUR)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
            elif segments_1[0] == [0, 0] and segments_1[2] == [0, 1]:
                graph.create_rectangle(5, 5, 105, 105, fill = RUTH_COLOUR, outline = RUTH_COLOUR)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
            elif segments_1[1] and segments_1[0][0] == 0 and 0 < segments_1[1] < 1:
                graph.create_rectangle(5, 5, 105, 105, fill = RUTH_COLOUR, outline = RUTH_COLOUR)
                graph.create_line(5, 105, segments_1[1] * 100 + 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [1, 1]:
                graph.create_rectangle(5, 5, 105, 105, fill = RUTH_COLOUR, outline = RUTH_COLOUR)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)
            elif not segments_1[2] and segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = RUTH_COLOUR, outline = RUTH_COLOUR)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [1, 1] and segments_1[2] == [0, 1]:
                graph.create_rectangle(5, 5, 105, 105, fill = RUTH_COLOUR, outline = RUTH_COLOUR)
                graph.create_line(5, 5, 105, 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(105, 5, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)               
            elif segments_1[1] and segments_1[0][1] == 1 and 0 < segments_1[1] < 1:
                graph.create_rectangle(5, 5, 105, 105, fill = RUTH_COLOUR, outline = RUTH_COLOUR)
                graph.create_line(5, 5, segments_1[1] * 100 + 5, 5, fill = NASH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 5, segments_1[1] * 100 + 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(segments_1[1] * 100 + 5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif segments_1[0] == [0, 1] and segments_1[2] == [0, 0]:
                graph.create_rectangle(5, 5, 105, 105, fill = RUTH_COLOUR, outline = RUTH_COLOUR)
                graph.create_line(5, 5, 5, 105, fill = NASH_COLOUR, width = 2)
                graph.create_line(5, 105, 105, 105, fill = NASH_COLOUR, width = 2)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
            elif not segments_1[0] and not segments_1[0]:
                graph.create_rectangle(5, 5, 105, 105, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 3, 7, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 3, 107, 7, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(3, 103, 7, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                graph.create_oval(103, 103, 107, 107, fill = NASH_COLOUR, outline = NASH_COLOUR)
                cells[0][0].config(fg = NASH_COLOUR)
                cells[0][1].config(fg = NASH_COLOUR)
                cells[1][0].config(fg = NASH_COLOUR)
                cells[1][1].config(fg = NASH_COLOUR)

    def display_information_about_special_expectations(self, special_expectations, expectations, probas):
        if expectations[0] != None :
            special_expectations[0].set('When Charlie uses proba q = ' + '{:.2f}'.format(probas[0]) +
                                ", Ruth's expectation is " + '{:.2f}'.format(expectations[0]))
        if expectations[1] != None:
            special_expectations[1].set('When Ruth uses proba p = ' + '{:.2f}'.format(probas[1]) +
                                ", Charlie's expectation is " + '{:.2f}'.format(expectations[1]))


class GameMatrix(Frame):
    def __init__(self):
        Frame.__init__(self, bd = 20)
        self.create_matrix()
        
    def create_matrix(self):
        # The payoffs will be analysed as if they were entered in the order (1, 0), (0, 0), (1, 1), (0, 1),
        # that is, from the pair that Ruth and Charlie would chose with probabilities p = 0 and q = 0, respectively,
        # to the pair that Ruth and Charlie would chose with probabilities p = 1 and q = 1, respectively, with in-between
        # first the pair that Ruth and Charlie would chose with probabilities p = 0 and q = 1, respectively, and
        # then the pair that Ruth and Charlie would chose with probabilities p = 1 and q = 0, respectively.
        # These four pairs of payoffs will be stored in self.cells[0][0], self.cells[0][1],
        # self.cells[1][0], self.cells[1][0], respectively.
        self.cells = [[None, None], [None, None]]
        self.payoffs = [[[None, None], [None, None]], [[None, None], [None, None]]]
        for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            self.cells[i][j] = Entry(self, bd = 4, width = 9, bg = CELL_COLOUR, fg = VALUE_COLOUR)
            self.cells[i][j].grid(column = i, row = 1 - j)
            self.cells[i][j].insert(0, '(0,0)')
        Label(self, text = 'Ruth', fg = RUTH_COLOUR).grid(columnspan = 2, pady = 5)
        Label(self, text = 'Charlie', fg = CHARLIE_COLOUR).grid(row = 0, rowspan = 2, column = 2, padx = 5)

    def restore_default_colours(self):
        for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            self.cells[i][j].config(bg = CELL_COLOUR, fg = VALUE_COLOUR)

    def get_payoffs(self):
        correct_input = True
        payoffs_pattern = re.compile('^ *\( *([+-]?(?:0|[1-9]\d*)) *, *([+-]?(?:0|[1-9]\d*)) *\) *$')
        for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            input = self.cells[i][j].get()
            parsed_input = payoffs_pattern.search(input)
            if not parsed_input:
                self.cells[i][j].config(bg = ERROR_COLOUR)
                correct_input = False
            else:
                self.cells[i][j].config(bg = CELL_COLOUR)
                self.payoffs[0][i][j] = int(parsed_input.groups()[0])
                self.payoffs[1][i][j] = int(parsed_input.groups()[1])
        if not correct_input:
            tkinter.messagebox.showerror('Incorrect input', 'Enter pairs of numbers separated by a comma '
                                                             'and surrounded by parentheses')
            return False
        return True


if __name__ == '__main__':
    NashEquilibriumCalculator().mainloop()
