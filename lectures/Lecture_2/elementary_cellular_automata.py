# Written by Eric Martin for COMP9021


from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
from random import randint


NB_OF_STEPS = 300
BACKGROUND_COLOUR = '#F5F5F5'
HISTORY_COLOUR = 'green'


class ElementaryCellularAutomata(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Elementary Cellular Automata')
        menubar = Menu()
        help_menu = Menu(menubar)
        menubar.add_cascade(label = 'Elementary Cellular Automaton Help', menu = help_menu)
        help_menu.add_command(label = 'Input', command = self.input_help)
        self.config(menu = menubar)
        
        self.input = Entry(self, width = 8)
        self.input.grid()
        self.previous_rule_number = None
        self.displaying_random_history = False
        self.shown_rule_number = StringVar()
        Label(self, width = 9, height = 1, textvariable = self.shown_rule_number, fg = 'magenta').grid(row = 0, column = 1)
        self.shown_rule = Canvas(self, width = 250, height = 50)
        self.shown_rule.grid(row = 0, column = 1, columnspan = 2, padx = (100, 0), pady = 10)
        Button(self, text = 'Display history from single 1', command = self.work_from_single_1).grid(padx = (40, 0))
        self.shown_related_rule_numbers = StringVar()
        Label(self, width = 87, height = 1, textvariable = self.shown_related_rule_numbers).grid(row = 1, column = 1)
        Button(self, text = 'Display history from random state',
               command = self.work_from_random_state).grid(row = 1, column = 2, padx = (0, 40))
        self.history = Canvas(self, width = NB_OF_STEPS * 4 + 3, height = NB_OF_STEPS * 2 + 5, bg = BACKGROUND_COLOUR)
        self.history.grid(columnspan = 3, pady = 20)
    
    def input_help(self):
        tkinter.messagebox.showinfo('Input',
            'The input should be a nonnegative integer at most '
            'equal to 255, represented either in base 10 or in base 2 with '
            'exactly 8 bits.')
    
    def work_from_single_1(self):
        input = self.get_rule()
        if input == False:
            return
        if input == None or self.previous_rule_number == self.rule_number:
            if self.displaying_history_from_single_1:
                return
        else:
            self.display_rule_information()
        self.history.delete(ALL)
        line = [[0] * (2 * NB_OF_STEPS + 1), [0] * (2 * NB_OF_STEPS + 1)]
        line[0][NB_OF_STEPS] = 1
        self.history.create_rectangle(2 * NB_OF_STEPS + 3, 5, 2 * NB_OF_STEPS + 5, 7, fill = HISTORY_COLOUR)
        a = False
        for i in range(1, NB_OF_STEPS - 1):
            line_a = line[a]
            line_not_a = line[not a]
            for j in range(NB_OF_STEPS - i - 1, NB_OF_STEPS + i + 2):
                line_not_a[j] = self.rule[line_a[j - 1], line_a[j], line_a[j + 1]]
            for j in range(0, NB_OF_STEPS - i - 1):
                line_not_a[j] = line_not_a[NB_OF_STEPS - i - 1]
            for j in range(NB_OF_STEPS + i + 2, 2 * NB_OF_STEPS + 1):
                line_not_a[j] = line_not_a[NB_OF_STEPS + i + 1]
            a = not a
            self.display_history_line(line, a, i, 0)
        line_a = line[a]
        line_not_a = line[not a]
        for j in range(1, 2 * NB_OF_STEPS):
            line_not_a[j] = self.rule[line_a[j - 1], line_a[j], line_a[j + 1]]
        self.display_history_line(line, not a, NB_OF_STEPS - 1, 0)
        self.previous_rule_number = self.rule_number
        self.displaying_history_from_single_1 = True

    def work_from_random_state(self):
        if self.get_rule() == False:
            return
        if self.previous_rule_number != self.rule_number:
            self.display_rule_information()
        self.history.delete(ALL)
        line = [[randint(0,1) for i in range(4 * NB_OF_STEPS - 2)], [0] * (4 * NB_OF_STEPS - 2)]
        self.display_history_line(line, 0, 0, NB_OF_STEPS - 2)
        a = False
        for i in range(1, NB_OF_STEPS):
            line_a = line[a]
            line_not_a = line[not a]
            for j in range(i, 4 * NB_OF_STEPS - 2 - i):
                line_not_a[j] = self.rule[line_a[j - 1], line_a[j], line_a[j + 1]]
            a = not a
            self.display_history_line(line, a, i, NB_OF_STEPS - 2)
        self.previous_rule_number = self.rule_number
        self.displaying_history_from_single_1 = False

    def display_history_line(self, line, a, i, offset):
        line_a = line[a]
        for j in range(1, 2 * NB_OF_STEPS):
            if line_a[j + offset]:
                self.history.create_rectangle(2 * j + 3, 2 * i + 5 , 2 * j + 5, 2 * i + 7, fill = HISTORY_COLOUR)
                    
    def get_rule(self):
        input = self.input.get()
        self.input.delete(0, END)
        if input == '':
            if self.previous_rule_number == None:
                tkinter.messagebox.showerror('Rule error', 'Please input a rule number')
                return False
            return None
        if not input.isdigit():
            self.warn_of_incorrect_input()
            return False
        if len(input) == 8:
            try:
                self.rule_number = int(input, 2)
            except ValueError:
                self.warn_of_incorrect_input()
                return False
            self.rule_bits = input
        else:
            if len(input) > 1 and input[0] == '0':
                self.warn_of_incorrect_input()
                return False
            self.rule_number = int(input)
            if self.rule_number >= 2 ** 8:
                self.warn_of_incorrect_input()
                return False
            self.rule_bits = '{:08b}'.format(self.rule_number)
        self.rule = {}
        for i in range(8):
            self.rule[i // 4, i // 2 % 2, i % 2] = int(self.rule_bits[7 - i])
        return True

    def display_rule_information(self):
        self.input.delete(0, END)
        self.shown_rule_number.set('Rule ' + str(self.rule_number))
        mirrored_rule_number = int(self.mirror(self.rule_bits), 2)
        complementary_rule_bits = self.rule_bits[::-1].translate(str.maketrans('01', '10'))
        complementary_rule_number = int(complementary_rule_bits, 2)
        mirrored_complementary_rule_number = int(self.mirror(complementary_rule_bits), 2)
        self.shown_related_rule_numbers.set('Mirrored rule: ' + str(mirrored_rule_number) +
                                            '            Complementary rule: ' + str(complementary_rule_number) +
                                            '            Mirrored complementary rule: ' +
                                            str(mirrored_complementary_rule_number))
        self.shown_rule.delete(ALL)
        self.shown_rule.create_line(5, 5, 245, 5)
        self.shown_rule.create_line(5, 25, 245, 25)
        self.shown_rule.create_line(5, 45, 245, 45)
        for i in range(9):
            self.shown_rule.create_line(i * 30 + 5, 5, i * 30 + 5, 45)
        for i in range(8):
            self.shown_rule.create_text(i * 30 + 20, 15, text = '{:03b}'.format(7 - i))
            self.shown_rule.create_text(i * 30 + 20, 35, text = self.rule_bits[i])

    def warn_of_incorrect_input(self):
        tkinter.messagebox.showerror('Rule error', 'Incorrect rule number')
        self.input.delete(0, END)

    def mirror(self, rule_bits):
        return ''.join([self.rule_bits[0], self.rule_bits[4], self.rule_bits[2], self.rule_bits[6],
                        self.rule_bits[1], self.rule_bits[5], self.rule_bits[3], self.rule_bits[7]])


if __name__ == '__main__':
    ElementaryCellularAutomata().mainloop()
