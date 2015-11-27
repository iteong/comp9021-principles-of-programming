# Written by Eric Martin for COMP9021

from tkinter import *
import tkinter.scrolledtext
import tkinter.messagebox
import tkinter.simpledialog


TAPE_COLOUR = '#FFFAF0'
NOT_RUNNING_FILL_COLOUR = '#FF1E00'
NOT_RUNNING_OUTLINE_COLOUR = '#980023'
RUNNING_FILL_COLOUR = '#25D500'
RUNNING_OUTLINE_COLOUR = '#007439'
CELL_COLOUR = '#8B7765'
LABEL_COLOUR = '#0B0974'
PROGRAM_BOX_COLOUR = '#F0FFF0'
PROGRAM_SELECTED_BOX_COLOUR = '#E0EEE0'
CELL_SIZE = 30
NB_OF_CELLS_WITHOUT_SCROLL = 21
CELL_PROPORTION_FOR_ENDSPACE = 2.2
MAX_NB_OF_STEPS = 1000
START = 0
STOP = 1
RESET = 2


class TuringMachineSimulator(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Turing Machine Simulator')
        menubar = Menu()
        help_menu = Menu(menubar)
        menubar.add_cascade(label = 'Turing Machine Simulator Help', menu = help_menu)
        help_menu.add_command(label = 'Tape', command = self.tape_help)
        help_menu.add_command(label = 'Program', command = self.program_help)
        help_menu.add_command(label = 'Execution', command = self.execution_help)
        self.config(menu = menubar)
        
        self.scrollable_tape = ScrollableTape()
        self.scrollable_tape.pack()
        self.program = Program()
        dashboard = Frame()
        self.state = State(dashboard)
        self.state.pack(padx = 20, side = LEFT)
        self.iteration = Iteration(dashboard)
        self.iteration.pack(padx = 20, side = LEFT)
        self.status = Status(dashboard, self.program)
        self.status.pack(padx = 20)
        dashboard.pack()
        buttons = Frame(bd = 20)
        self.next_phase_button = Button(buttons, text = 'Start', width = 5, command = self.act)
        self.next_phase_button.pack(padx = 30, side = LEFT)
        self.step_button = Button(buttons, text = 'Step', command = self.step, state = DISABLED)
        self.step_button.pack(padx = 30, side = LEFT)
        self.continue_button = Button(buttons, text = 'Continue', command = self.run_further, state = DISABLED)
        self.continue_button.pack(padx = 30)
        buttons.pack()
        self.program.pack()
        self.next_phase = START
    
    def tape_help(self):
        tkinter.messagebox.showinfo('Tape',
            'The tape always contains an "origin" cell.\n\n'
            'Control clicking to the right or to the left of the current '
            'rightmost or leftmost cell, respectively, adds a new cell.\n\n'
            'Control clicking on the current rightmost or leftmost added cell '
            'removes it.\n\n'''
            'Clicking on any cell flips the bit it contains from 1 to 0 '
            'or from 0 to 1.')
    
    def program_help(self):
        tkinter.messagebox.showinfo('Program',
            'A program is a set of instructions of the form\n'
            '  _state1_ _bit1_ _state2_ _bit2_ _dir_\n'
            'where _state1_ and _state2_ have to be alphanumeric words '
            'with at most 8 characters, _bit1_ and _bit2_ have to be 0 or 1, '
            'and _dir_ has to be L or R.\n\n'
            'When the TM machine is in state _state1_ with its head '
            'pointing to a cell containing _bit1_, then it changes '
            '_bit1_ to _bit2_ in that cell, modifies its state to _state2_, '
            'and moves its head one cell to the right or to the left '
            'as determined by _dir_.\n\n'
            'The TM machine is supposed to be deterministic, hence '
            'the program should not contain two instructions starting with '
            'the same pair (_state1_,_bit1_).\n\n'
            'The program can contain comments, namely, lines starting with #.')
    
    def execution_help(self):
        tkinter.messagebox.showinfo('Execution',
            'When the leftmost button displays Start, the status indicator is red, '
            'the tape can be modified, the program can be edited, the Step and '
            'Continue buttons are disabled, and no State or Iteration is displayed.\n\n'
            'Once this button has been pressed, it displays Stop, the status '
            'indicator is green, the tape cannot be modified, the program cannot be '
            'edited, and the current State and Iteration are displayed.\n\n'
            'When execution stops, either because no instruction can be executed '
            'or because Stop has been pressed, the Step and Continue buttons are '
            'disabled and the leftmost button displays Reset; it has to be pressed '
            'to restore the tape in its initial configuration, '
            'with only the "origin" cell containing 1.\n\n'
            'Pressing the Start button prompts the user for an initial state, which '
            'has to be an alphanumeric word with at most 8 characters, and '
            'commences execution provided at least one cell contains 1, '
            'in which case the head initially points to the leftmost cell '
            'containing 1.\n\n'
            'The Step button executes one instruction, if possible; '
            'otherwise execution stops.\n\n'
            'The Continue buttom executes up to 1,000 instructions, '
            'if possible; otherwise execution stops.\n\n'
            'The Stop button allows one to start a new excution in case it is '
            'either not desirable or not possible to terminate execution '
            'with a sequence of clicks on the Step or Continue buttons.')

    def act(self):
        if self.next_phase == START:
            self.start()
        elif self.next_phase == STOP:
            self.stop()
        else:
            self.reset()
    
    def start(self):
        if not self.program.read_instructions():
            return
        initial_state = tkinter.simpledialog.askstring('Starting program', 'Enter initial state: ')
        if initial_state == None:
            return
        if not StateName(initial_state).check_syntactic_validity():
            return
        for i in range(len(self.scrollable_tape.cells[0]) - 1, -1, -1):
            if self.scrollable_tape.bits[0][i] == 1:
                self.scrollable_tape.tape.itemconfig(self.scrollable_tape.cells[0][i],
                                                     fill = 'red', font = ('normal', 0, 'bold'))
                self.current_index = -i
                break
        else:
            for i in range(1, len(self.scrollable_tape.cells[1])):
                if self.scrollable_tape.bits[1][i] == 1:
                    self.scrollable_tape.tape.itemconfig(self.scrollable_tape.cells[1][i],
                                                             fill = 'red', font = ('normal', 0, 'bold'))
                    self.current_index = i
                    break
            else:
                tkinter.messagebox.showerror('Tape error', 'Cannot run, no bit is set to 1 in tape')
                return
        self.status.signal(True)
        self.step_button.config(state = NORMAL)
        self.continue_button.config(state = NORMAL)
        self.next_phase = STOP
        self.next_phase_button.config(text = 'Stop')
        self.current_bit = 1
        self.current_state = initial_state
        self.current_iteration = 0
        self.iteration.update(0)
        self.state.update(initial_state)
    
    def reset(self):
        self.scrollable_tape.reset()
        self.state.update('')
        self.iteration.update('')
        self.next_phase = START
        self.next_phase_button.config(text = 'Start')
   
    def step(self):
        state, bit = self.current_state, self.current_bit
        if (state, bit) not in self.program.instructions.keys():
            self.status.signal(False)
            self.next_phase = RESET
            self.next_phase_button.config(text = 'Reset')
            self.step_button.config(state = DISABLED)
            self.continue_button.config(state = DISABLED)
            return
        new_state, new_bit, direction = self.program.instructions[state, bit]
        self.state.update(new_state)
        self.current_iteration += 1
        self.iteration.update(self.current_iteration)
        i = self.current_index
        side = i > 0
        j = abs(i)
        self.scrollable_tape.bits[side][j] = new_bit
        if i == 0:
            self.scrollable_tape.bits[1 - side][0] = new_bit
        self.scrollable_tape.tape.itemconfig(
            self.scrollable_tape.cells[side][j], text = new_bit,
            fill = 'black', font = ('normal', 0, 'normal'))
        i += direction
        side = i > 0
        j = abs(i)
        if j >= len(self.scrollable_tape.bits[side]):
            self.scrollable_tape.add_cell_to_end(side)
        self.scrollable_tape.tape.itemconfig(
            self.scrollable_tape.cells[side][j],
            fill = 'red', font = ('normal', 0, 'bold'))
        self.current_bit = self.scrollable_tape.bits[side][j]
        self.current_index = i
        self.current_state = new_state
    
    def run_further(self):
        if self.next_phase == STOP:
            bound = self.current_iteration + MAX_NB_OF_STEPS
        while self.next_phase == STOP and self.current_iteration < bound:
            self.step()
    
    def stop(self):
        self.status.signal(False)
        self.next_phase = RESET
        self.next_phase_button.config(text = 'Reset')
        self.step_button.config(state = DISABLED)
        self.continue_button.config(state = DISABLED)


class ScrollableTape(Frame):
    def __init__(self):
        Frame.__init__(self, bd = 10, padx = 20)
        self.set_original_conditions()
        w = (NB_OF_CELLS_WITHOUT_SCROLL + 2 * CELL_PROPORTION_FOR_ENDSPACE) * CELL_SIZE
        self.tape = Canvas(self, width = w, height = CELL_SIZE + 1, bg = TAPE_COLOUR)
        self.draw_minimal_tape()
        self.tape.grid(row = 0)
        scrollbar = Scrollbar(self, orient = HORIZONTAL, command = self.tape.xview)
        self.tape.config(xscrollcommand = scrollbar.set)
        scrollbar.grid(row = 1, sticky = EW)
        self.tape.bind('<1>', self.flip_bit)
        self.tape.bind('<Control-1>', self.add_or_remove_cell)

    def set_original_conditions(self):
        self.max_indexes = [0, 0]
        self.bits = [[1], [1]]
        self.cells = [[None], [None]]
        self.lines = [[None], [None]]

    def determine_left_boundary(self):
        return -(self.max_indexes[0] + CELL_PROPORTION_FOR_ENDSPACE) * CELL_SIZE

    def determine_right_boundary(self):
        return (max(NB_OF_CELLS_WITHOUT_SCROLL, self.max_indexes[1]) + CELL_PROPORTION_FOR_ENDSPACE) * CELL_SIZE

    def draw_minimal_tape(self):
        left_boundary = self.determine_left_boundary()
        right_boundary = self.determine_right_boundary()
        self.tape.config(scrollregion = (left_boundary, -(CELL_SIZE / 2), right_boundary, CELL_SIZE + 1))
        self.tape.delete(ALL)
        self.tape.create_line(-0.5 * CELL_SIZE, 0, -0.5 * CELL_SIZE, CELL_SIZE, width = 2, fill = CELL_COLOUR)
        self.cells[0][0] = self.tape.create_text(0, CELL_SIZE / 2, text = self.bits[0][0])
        self.tape.create_line(0.5 * CELL_SIZE, 0, 0.5 * CELL_SIZE, CELL_SIZE, width = 2, fill = CELL_COLOUR)
        self.draw_horizontal_lines(left_boundary, right_boundary)

    def draw_horizontal_lines(self, left_boundary, right_boundary):
        self.tape.create_line(left_boundary, 0, right_boundary - left_boundary, 0, width = 3, fill = CELL_COLOUR)
        self.tape.create_line(left_boundary, CELL_SIZE, right_boundary, CELL_SIZE, width = 3, fill = CELL_COLOUR)

    def add_cell_to_end(self, side):
        i = len(self.bits[side])
        if i > self.max_indexes[side]:
            self.max_indexes[side] = i
            left_boundary = self.determine_left_boundary()
            right_boundary = self.determine_right_boundary()
            self.tape.config(scrollregion = (left_boundary, -(CELL_SIZE / 2), right_boundary, CELL_SIZE + 1))
            self.draw_horizontal_lines(left_boundary, right_boundary)
        self.bits[side].append(0)
        self.cells[side].append(None)
        self.lines[side].append(None)
        s = side * 2 - 1
        self.cells[side][i] = self.tape.create_text(i * s * CELL_SIZE, CELL_SIZE / 2, text = 0)
        self.lines[side][i] = self.tape.create_line(s * (i + 0.5) * CELL_SIZE, 0, s * (i + 0.5) * CELL_SIZE, CELL_SIZE,
                                                    width = 2, fill = CELL_COLOUR)
      
    def flip_bit(self, event):
        if not self.master.next_phase == START:
            return
        if 0 <= event.y <= CELL_SIZE:
            i = round(self.tape.canvasx(event.x) / CELL_SIZE)
            side = i > 0
            i = abs(i)
            if 0 <= i < len(self.cells[side]):
                self.bits[side][i] = 1 - self.bits[side][i]
                self.tape.itemconfig(self.cells[side][i], text = self.bits[side][i])

    def add_or_remove_cell(self, event):
        if not self.master.next_phase == START:
            return
        if 0 <= event.y <= CELL_SIZE:
            i = round(event.widget.canvasx(event.x) / CELL_SIZE)
            if i == 0:
                return
            side = i > 0
            i = abs(i)
            if i == len(self.bits[side]) - 1:
                self.tape.delete(self.cells[side][i])
                self.tape.delete(self.lines[side][i])
                del self.bits[side][i]
                del self.cells[side][i]
                del self.lines[side][i]                
            elif i == len(self.bits[side]):
                self.add_cell_to_end(side)

    def reset(self):
        del self.cells[0][1:]
        del self.cells[1][1:]
        del self.bits[0][1:]
        del self.bits[1][1:]
        del self.lines[0][1:]
        del self.lines[1][1:]
        self.set_original_conditions()
        self.max_indexes = [0, 0]
        self.draw_minimal_tape()

        
class Program(Frame):
    def __init__(self):
        Frame.__init__(self, bd = 30)
        Label(self, text = 'Program', fg = LABEL_COLOUR, bd = 10).pack()
        self.source_code = tkinter.scrolledtext.ScrolledText(self, width = 23, height = 20,
                                                             highlightbackground = PROGRAM_BOX_COLOUR,
                                                             highlightcolor = PROGRAM_SELECTED_BOX_COLOUR)
        self.source_code.pack()
    
    def read_instructions(self):
        self.instructions = {}
        source_instructions = self.source_code.get(0.0, END)
        for instruction in source_instructions.splitlines():
            quintuple = instruction.split()
            if len(quintuple) == 0 or quintuple[0][0] == '#':
                continue
            if len(quintuple) != 5:
                tkinter.messagebox.showerror('Instruction error', '"{}" is not a quintuple'.format(instruction))
                return False
            state, bit, new_state, new_bit, direction = quintuple
            if not StateName(state).check_syntactic_validity():
                return False
            if not Bit(bit).check_syntactic_validity():
                return False
            if not StateName(new_state).check_syntactic_validity():
                return False
            if not Bit(new_bit).check_syntactic_validity():
                return False
            if direction != 'L' and direction != 'R':
                tkinter.messagebox.showerror('Instruction error', '"{}" should be "L" or "R"'.format(direction))
                return False
            if (state, int(bit)) in self.instructions:
                tkinter.messagebox.showerror('Instruction error', 'More than one instruction for pair "({}, {})"'.format(state, bit))
                return False
            self.instructions[(state, int(bit))] = (new_state, int(new_bit), (direction == 'R') * 2 - 1)
        return True


class StateName(str):
    def check_syntactic_validity(self):
        if self == None:
            tkinter.messagebox.showerror('State name error', 'State name cannot be "None"')
            return False
        if len(self) > 8:
            tkinter.messagebox.showerror('State name error', '"{}" contains more than 8 characters'.format(self))
            return False
        if not self.isalnum():
            tkinter.messagebox.showerror('State name error', '"{}" not all nonalphanumeric'.format(self))
            return False
        return True


class Bit(str):
    def check_syntactic_validity(self):
        if self != '0' and self != '1':
            tkinter.messagebox.showerror('Instruction error', '"{}" should be "0" or "1"'.format(self))
            return False
        return True


class State(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text = 'State: ', fg = LABEL_COLOUR).pack(side = LEFT)
        self.state = StringVar()
        Label(self, width = 8, textvariable = self.state).pack()

    def update(self, s):
        self.state.set(s)


class Iteration(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text = '  Iteration: ', fg = LABEL_COLOUR).pack(side = LEFT)
        self.iteration = StringVar()
        Label(self, width = 4, height = 1, textvariable = self.iteration).pack()

    def update(self, i):
        self.iteration.set(i)


class Status(Canvas):
    def __init__(self, master, program):
        Canvas.__init__(self, master, width = 20, height = 20)
        self.status = self.create_oval(10, 10, 20, 20, fill = NOT_RUNNING_FILL_COLOUR, outline = NOT_RUNNING_OUTLINE_COLOUR)
        self.pack()
        self.program = program
        
    def signal(self, running):
        if running:
            self.itemconfig(self.status, fill = RUNNING_FILL_COLOUR, outline = RUNNING_OUTLINE_COLOUR)
            self.program.source_code.config(state = 'disabled')
        else:
            self.itemconfig(self.status, fill = NOT_RUNNING_FILL_COLOUR, outline = NOT_RUNNING_OUTLINE_COLOUR)
            self.program.source_code.config(state = 'normal')            

        
if __name__ == '__main__':
    TuringMachineSimulator().mainloop()
