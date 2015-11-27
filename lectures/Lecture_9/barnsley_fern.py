# Written by Eric Martin for COMP9021

from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
from random import choice


NB_OF_ITERATIONS = 20000
DIM = 600
HALF_DIM = DIM // 2
FERN_COLOUR = '#006400'
ERROR_COLOUR = '#FFCCCC'


class BarnsleyFern(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Barnsley Fern')
        menubar = Menu()
        help_menu = Menu(menubar)
        menubar.add_cascade(label = 'Barnsley Fern Help', menu = help_menu)
        help_menu.add_command(label = 'Affine transformations', command = self.affine_transformations_help)
        help_menu.add_command(label = 'Displayed parameters', command = self.displayed_parameters_help)
        help_menu.add_command(label = 'Fern species', command = self.fern_species_help)
        self.config(menu = menubar)

        fern_selection_board = Frame(bd = 20)
        predefined_ferns_button = Menubutton(fern_selection_board, text = 'Predefined ferns')
        predefined_ferns_button.pack(padx = 30, pady = 30)
        predefined_ferns = Menu(predefined_ferns_button)
        predefined_ferns.add_command(label = 'Black Spleenwort',
                                     command = lambda fern_species = 'Black Spleenwort' : self.display_fern(fern_species))
        predefined_ferns.add_command(label = 'Culcita',
                                     command = lambda fern_species = 'Culcita' : self.display_fern(fern_species))
        predefined_ferns.add_command(label = 'Cyclosorus',
                                     command = lambda fern_species = 'Cyclosorus' : self.display_fern(fern_species))
        predefined_ferns_button.config(menu = predefined_ferns)
        fern_parameters_board = FernParametersBoard()
        self.drawing = Drawing(fern_parameters_board)
        self.drawing.pack(padx = 30, side = LEFT)
        fern_selection_board.pack()
        fern_parameters_board.pack()
        draw_buttons = Frame(bd = 20)
        Button(draw_buttons, text = 'Draw custom fern',
               command = lambda fern_species = 'Custom' : self.display_fern(fern_species)).pack(padx = 20, side = LEFT)
        draw_buttons.pack()
        self.displayed_fern = StringVar()
        Label(draw_buttons, textvariable = self.displayed_fern, width = 16, fg = FERN_COLOUR).pack(pady = 40)
        self.displayed_fern.set('Black Spleenwort')

    def affine_transformations_help(self):
        tkinter.messagebox.showinfo('Affine transformations',
            'A fern is a fixed point A of four affine transformations T1, T2, T3 and T4, \n'
            'each of wich maps a point (x, y) to (ax + by + e, cx + dy + f) for some '
            'real numbers a, b, c, d, e and f, i.e., A is the union of T1(A), T2(A), T3(A) and T4(A).\n\n'
            'Denoting by L and R the largest left and right leaflets, respectively, '
            'T2, T3 and T4 are determined by the image of 3 noncolinear points:\n'
            ' - T2 maps the tip of the fern to itself and the tips of L and R to the tips '
            'of the second largest left and right leaflets of the fern, respectively.\n'
            ' - T3 and T4 map the bottom of the stem of the fern to the bottom of the stems '
            'of L and R and the tips of the largest left and right leaflets of the fern to the tips '
            'of the largest left and right leaflets of L and R, respectively.\n'
            ' - As for T1, it is best described as projecting all points of the fern on the y-axis '
            'before applying a contraction.')

    def displayed_parameters_help(self):
        tkinter.messagebox.showinfo('Displayed parameters',
            'For each of T1, T2, T3 and T4, the parameters are displayed as\n'
            '    a    b    e\n'
            '    c    d    f\n\n'
            'The number to the right represents the probability that the corresponding '
            'transformation be applied to the current point, starting from point (0,0), '
            'located at the bottom of the stem of the fern.\n\n'
            'Factor can be used to scale the picture the fern up or down.')

    def fern_species_help(self):
        tkinter.messagebox.showinfo('Fern species',
            'Three predefined fern species can be selected, with the corresponding parameters '
            'being automatically displayed. The parameters can be set of any value to display '
            'a "custom" fern, provided that:\n'
            ' - a, b, c, d, e and f are floating point numbers;\n'
            ' - the probabilities are nonnegative integers that sum up to 100;\n'
            ' - the scaling factor is a strictly positive integer.')

    def display_fern(self, fern_species):
        self.displayed_fern.set(fern_species)
        self.drawing.display_fern(fern_species)
        
    
class Drawing(Frame):
    def __init__(self, fern_parameters_board):
        Frame.__init__(self, padx = 20, pady = 20)
        self.fern_parameters_board = fern_parameters_board
        self.drawing = Canvas(self, width = DIM, height = DIM + 50)
        self.drawing.pack()
        self.fern = BlackSpleenwort()
        self.draw_fern()

    def display_fern(self, fern_species):
        if fern_species == 'Custom':
            self.fern = Fern()
            self.fern_parameters_board.factor.config(bg = 'white')
            for n in range(4):
                self.fern_parameters_board.probas[n].config(bg = 'white')
                for i in range(2):
                    self.fern_parameters_board.translation_vectors[n][i].config(bg = 'white')
                    for j in range(2):
                        self.fern_parameters_board.linear_coefficients[n][i][j].config(bg = 'white')
            incorrect_input = False
            try:
                self.fern.factor = int(self.fern_parameters_board.factor.get())
            except:
                self.fern_parameters_board.factor.config(bg = ERROR_COLOUR)
                incorrect_input = True
            if self.fern.factor <= 0:
                self.fern_parameters_board.factor.config(bg = ERROR_COLOUR)
                incorrect_input = True                    
            for n in range(4):
                try:
                    self.fern.probas[n] = int(self.fern_parameters_board.probas[n].get())
                except:
                    self.fern_parameters_board.probas[n].config(bg = ERROR_COLOUR)
                    incorrect_input = True
                if self.fern.probas[n] < 0:
                    self.fern_parameters_board.probas[n].config(bg = ERROR_COLOUR)
                    incorrect_input = True                    
                for i in range(2):
                    try:
                        self.fern.translation_vectors[n][i] = \
                            float(self.fern_parameters_board.translation_vectors[n][i].get())
                    except:
                        self.fern_parameters_board.translation_vectors[n][i].config(bg = ERROR_COLOUR)
                        incorrect_input = True
                    for j in range(2):
                        try:
                            self.fern.linear_coefficients[n][i][j] =\
                                float(self.fern_parameters_board.linear_coefficients[n][i][j].get())
                        except:
                            self.fern_parameters_board.linear_coefficients[n][i][j].config(bg = ERROR_COLOUR)
                            incorrect_input = True
            if incorrect_input:
                return
            if sum(self.fern.probas) != 100:
                for n in range(4):
                    self.fern_parameters_board.probas[n].config(bg = ERROR_COLOUR)
                tkinter.messagebox.showerror('Incorrect input', 'Probabilities should sum to 100')
                return
        else:
            if fern_species == 'Black Spleenwort':
                self.fern = BlackSpleenwort()
            elif fern_species == 'Culcita':
                self.fern = Culcita()
            elif fern_species == 'Cyclosorus':
                self.fern = Cyclosorus()
            self.fern_parameters_board.update_parameters(self.fern)       
        self.drawing.delete(ALL)
        self.draw_fern()
        

    def draw_fern(self):
        weighted_parts_of_fern = []
        for i in range(4):
            weighted_parts_of_fern += [i] * self.fern.probas[i]
        point = (0, 0)
        for i in range(NB_OF_ITERATIONS):
            part_of_fern = choice(weighted_parts_of_fern)
            point = self.transform(self.fern.linear_coefficients[part_of_fern],
                                   self.fern.translation_vectors[part_of_fern], *point)

    def transform(self, linear_transformation_matrix, translation_vector, x, y):
        new_x = linear_transformation_matrix[0][0] * x + linear_transformation_matrix[0][1] * y + translation_vector[0]
        new_y = linear_transformation_matrix[1][0] * x + linear_transformation_matrix[1][1] * y + translation_vector[1]
        x, y = new_x, new_y
        self.draw_point(x, y)
        return x, y

    def draw_point(self, x, y):
        x *= self.fern.factor
        y *= self.fern.factor
        self.drawing.create_oval(HALF_DIM + x - 0.3, DIM - y - 0.3, HALF_DIM + x + 0.3, DIM - y + 0.3,
                              fill = FERN_COLOUR, outline = FERN_COLOUR)
        
                
class Fern:
    def __init__(self):
        self.linear_coefficients = [[[None, None], [None, None]], [[None, None], [None, None]],
                                    [[None, None], [None, None]], [[None, None], [None, None]]]
        self.translation_vectors = [[None, None], [None, None], [None, None], [None, None]]
        self.probas = [None, None, None, None]
        self.factor = None


class BlackSpleenwort(Fern):
    linear_coefficients = [[[0, 0], [0, 0.16]], [[0.85, 0.04], [-0.04, 0.85]],
                           [[0.2, -0.26], [0.23, 0.22]], [[-0.15, 0.28], [0.26, 0.24]]]
    translation_vectors = [[0, 0], [0, 1.6], [0, 1.6], [0, 0.44]]
    probas = [1, 85, 7, 7]
    factor = DIM // 12
    
    def __init__(self):
        self.factor = BlackSpleenwort.factor
        for n in range(4):
            self.probas[n] = BlackSpleenwort.probas[n]
            for i in  range(2):
                self.translation_vectors[n][i] = BlackSpleenwort.translation_vectors[n][i]
                for j in range(2):
                    self.linear_coefficients[n][i][j] = BlackSpleenwort.linear_coefficients[n][i][j]


class Culcita(Fern):
    linear_coefficients = [[[0, 0], [0, 0.25]], [[0.85, 0.02], [-0.02, 0.83]],
                           [[0.09, -0.28], [0.30, 0.11]], [[-0.09, 0.28], [0.3, 0.09]]]
    translation_vectors = [[0, -0.14], [0, 1], [0, 0.6], [0, 0.7]]
    probas = [2, 84, 7, 7]
    factor = DIM // 6
    
    def __init__(self):
        self.factor = Culcita.factor
        for n in range(4):
            self.probas[n] = Culcita.probas[n]
            for i in  range(2):
                self.translation_vectors[n][i] = Culcita.translation_vectors[n][i]
                for j in range(2):
                    self.linear_coefficients[n][i][j] = Culcita.linear_coefficients[n][i][j]


class Cyclosorus(Fern):
    linear_coefficients = [[[0, 0], [0, 0.25]], [[0.95, 0.005], [-0.005, 0.93]],
                           [[0.035, -0.2], [0.16, 0.04]], [[-0.04, 0.2], [0.16, 0.04]]]
    translation_vectors = [[0, -0.4], [-0.002, 0.5], [-0.09, 0.02], [0.083, 0.12]]
    probas = [2, 94, 2, 2]
    factor = DIM // 8
    
    def __init__(self):
        self.factor = Cyclosorus.factor
        for n in range(4):
            self.probas[n] = Cyclosorus.probas[n]
            for i in  range(2):
                self.translation_vectors[n][i] = Cyclosorus.translation_vectors[n][i]
                for j in range(2):
                    self.linear_coefficients[n][i][j] = Cyclosorus.linear_coefficients[n][i][j]


class FernParametersBoard(Frame):
    def __init__(self):
        Frame.__init__(self, bd = 20)
        fern = BlackSpleenwort()
        self.linear_coefficients = [[[None, None], [None, None]], [[None, None], [None, None]],
                                    [[None, None], [None, None]], [[None, None], [None, None]]]
        self.translation_vectors = [[None, None], [None, None], [None, None], [None, None]]
        self.probas = [None, None, None, None]
        for n in range(4):
            if n == 0:
                text_label = 'Stem'
            elif n == 1:
                text_label = 'Upper leaflets'
            elif n == 2:
                text_label = 'Lower left leaflet'
            else:
                text_label = 'Lower right leaflet'               
            Label(self, text = text_label).grid(row = 3 * n, columnspan = 4, pady = 5)
            for i in range(2):
                for j in range(2):
                    self.linear_coefficients[n][i][j] = Entry(self, bd = 1, width = 5)
                    self.linear_coefficients[n][i][j].grid(row = 3 * n + i + 1, column = j)
                    self.linear_coefficients[n][i][j].insert(0, fern.linear_coefficients[n][i][j])
                self.translation_vectors[n][i] = Entry(self, bd = 1, width = 5)
                self.translation_vectors[n][i].grid(row = 3 * n + i + 1, column = 2, padx = 15)
                self.translation_vectors[n][i].insert(0, fern.translation_vectors[n][i])
            self.probas[n] = Entry(self, bd = 1, width = 3)
            self.probas[n].grid(row = 3 * n + 1, rowspan = 2, column = 3, padx = 25)
            self.probas[n].insert(0, fern.probas[n])
        Label(self, text = 'Factor').grid(row = 12, pady = 40)
        self.factor = Entry(self, bd = 1, width = 4)
        self.factor.grid(row = 12, column = 1)
        self.factor.insert(0, fern.factor)

    def update_parameters(self, fern):
        self.factor.delete(0, END)
        self.factor.insert(0, fern.factor)
        for n in range(4):
            self.probas[n].delete(0, END)
            self.probas[n].insert(0, fern.probas[n])
            for i in range(2):
                self.translation_vectors[n][i].delete(0, END)
                self.translation_vectors[n][i].insert(0, fern.translation_vectors[n][i])
                for j in range(2):
                    self.linear_coefficients[n][i][j].delete(0, END)
                    self.linear_coefficients[n][i][j].insert(0, fern.linear_coefficients[n][i][j])
                
 
if __name__ == '__main__':
    BarnsleyFern().mainloop()
