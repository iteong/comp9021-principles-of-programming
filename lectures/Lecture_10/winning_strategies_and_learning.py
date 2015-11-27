# Written by Eric Martin for COMP9021

from tkinter import *
import tkinter.messagebox
from copy import deepcopy
from random import randrange


BLACK = 0
RED = 1
FREE = 2
ON_TRACK_TO_LOSE = 0
ON_TRACK_TO_WIN = 1
ON_TRACK_FOR_LUCKY_WIN = 2
WIDTH = 36
THIRD_WIDTH = WIDTH // 3
OFFSET = WIDTH // 2

class WinningStrategy(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Winning Strategies and Learning')
        menubar = Menu()
        help_menu = Menu(menubar)
        menubar.add_cascade(label = 'Winning Strategies and Learning Help', menu = help_menu)
        help_menu.add_command(label = 'Rules of the game', command = self.rules_help)
        help_menu.add_command(label = 'Search tree', command = self.search_tree_help)
        help_menu.add_command(label = 'Opponent', command = self.opponent_help)
        help_menu.add_command(label = 'Learning', command = self.learning_help)
        self.config(menu = menubar)

        self.search_tree = SearchTree()
        DisplayedSearchTree(self.search_tree.tree).grid()
        SimulationBoard(self.search_tree.tree).grid(row = 0, column = 1)

    def rules_help(self):
        tkinter.messagebox.showinfo('Rules of the game',
            "Pawns can move forward or take an opponent's pawn diagonally.\n\n"
            'Black or red wins when one of its pawns has reached the opposite line, '
            'or the opponent cannot move.')

    def search_tree_help(self):
        tkinter.messagebox.showinfo('Search tree',
            "Click on a state to expand the tree and display the opponent's possible moves, if any.\n"
            'Control click on a state to collpase the tree and hide all displayed possible subsequent states, if any.\n\n'
            'The outline of a state is boldfaced if that state is part of a winning strategy; it can only be for the black player.\n'
            'The outline of a state is dashed boldfaced if that state is part of a winning strategy at some point in the game, '
            'but not from its beginning; it can be for either the black or the red player.')

    def opponent_help(self):
        tkinter.messagebox.showinfo('Opponent',
            'The opponent is the red player.\n\n'
            'The random opponent randomly choses a state amongst all possible next states.\n\n'
            'The good opponent randomly choses a state amongst all possible next states in case '
            'no such state is part of a winning strategy at that point in the game; otherwise, '
            'it randomly chooses a state amongst all possible next states that happen to be part '
            'of a winning strategy at that point in the game.')

    def learning_help(self):
        tkinter.messagebox.showinfo('Learning',
            'The learner is the black player.\n\n'
            'The learner randomly choses a state amongst all possible next states.\n'
            "When the opponent wins, the learner eliminates the state which made that oppent's last move "
            'possible from its future choices.\n'
            'When the opponent plays, does not win, but all possible next states for the learner have been eliminated, '
            "then the learner 'gives up' and eliminates the state which made that oppent's move possible from its future choices.\n\n"
            'Learning cannot be improved when enough states have been eliminated and all possible moves from the learner '
            'are part of a winning strategy.')


class State:
    def __init__(self, depth = 0, displayed = False, state = None):
        self.depth = depth
        self.expected_outcome = ON_TRACK_TO_LOSE
        self.displayed = displayed
        self.state = state
        self.code = self.code_state()
        self.x = 0
        self.y = 0
        self.next_states = []

    def code_state(self):
        code = 0
        for i in range(3):
            for j in range(3):
                code = code * 3 + self.state[i][j]
        return code

    def display_state(self, canvas, line):
        for i in range(3):
            for j in range(3):
                if self.depth % 2:
                    displayed_colour = 'red'
                else:
                    displayed_colour = 'black'
                if self.expected_outcome == ON_TRACK_TO_LOSE:
                    displayed_width = 1
                else:
                    displayed_width = 2
                if self.expected_outcome == ON_TRACK_FOR_LUCKY_WIN:
                    expected_lucky_outcome = (3, )
                else:
                    expected_lucky_outcome = 1
                x = OFFSET + self.depth * WIDTH
                y = OFFSET + line * WIDTH
                canvas.create_polygon(x + 1, y + 1, x + WIDTH - 1, y + 1, x + WIDTH - 1, y + WIDTH - 1, x + 1, y + WIDTH - 1,
                                      fill = '', outline = displayed_colour, width = displayed_width, dash = expected_lucky_outcome, dashoff = 1)
                if self.state[i][j] == BLACK:
                    colour = 'black'
                elif self.state[i][j] == RED:
                    colour = 'red'
                else:
                    colour = 'white'
                canvas.create_oval(x + j * THIRD_WIDTH + 3, y + i * THIRD_WIDTH + 3, x + j * THIRD_WIDTH + 8, y + i * THIRD_WIDTH + 8,
                                   fill = colour, outline = 'black')
                self.x = x
                self.y = y


class SearchTree:
    def __init__(self):
        self.tree = State(displayed = True, state = [[BLACK] * 3, [FREE] * 3, [RED] * 3])
        self.complete_search_tree(self.tree)
        self.determine_winning_strategy(self.tree)
        self.identify_defeated_states(self.tree)
        for subtree in self.tree.next_states:
            self.identify_defeated_states(subtree)
        
    def complete_search_tree(self, tree):
        next_color = 1 - tree.depth % 2
        next_states = self.determine_next_states(tree.state, next_color)
        if next_states:
            subtrees = [State(depth = tree.depth + 1, state = next_state) for next_state in next_states]
            tree.next_states = subtrees
            for subtree in subtrees:
                self.complete_search_tree(subtree)

    def determine_next_states(self, state, colour):
        arrival_line = (1 - colour) * 2
        if colour in state[arrival_line] or 1 - colour in state[2 - arrival_line]:
            return None
        starting_line = colour * 2
        direction = arrival_line - 1
        next_states = []
        for i in [starting_line, 1]:
            for j in [0, 1, 2]:
                if state[i][j] == colour and state[i + direction][j] == FREE:
                    self.extend_states(next_states, state, i, j, i + direction, j, colour)
            for j in [0, 1]:
                if state[i][j] == colour and state[i + direction][j + 1] == 1 - colour:
                    self.extend_states(next_states, state, i, j, i + direction, j + 1, colour)
            for j in [1, 2]:
                if state[i][j] == colour and state[i + direction][j - 1] == 1 - colour:
                    self.extend_states(next_states, state, i, j, i + direction, j - 1, colour)
        return next_states
                        
    def extend_states(self, next_states, state, i1, j1, i2, j2, color):
        next_state = deepcopy(state)
        next_state[i1][j1] = FREE
        next_state[i2][j2] = color
        next_states.append(next_state)

    def determine_winning_strategy(self, tree):
        if not tree.next_states:
            tree.expected_outcome = ON_TRACK_TO_WIN
        else:
            for subtree in tree.next_states:
                self.determine_winning_strategy(subtree)
            if all(subtree.expected_outcome == ON_TRACK_TO_LOSE for subtree in tree.next_states):
                tree.expected_outcome = ON_TRACK_TO_WIN

    def identify_defeated_states(self, tree):
        if not tree.next_states:
            return
        if tree.expected_outcome != ON_TRACK_TO_WIN:
            for subtree in tree.next_states:
                for subsubtree in subtree.next_states:
                    if subsubtree.expected_outcome == ON_TRACK_TO_WIN:
                        subsubtree.expected_outcome = ON_TRACK_FOR_LUCKY_WIN
        for subtree in tree.next_states:
            for subsubtree in subtree.next_states:
                self.identify_defeated_states(subsubtree)

    
class DisplayedSearchTree(Frame):
    def __init__(self, tree):
        Frame.__init__(self, pady = 20)
        self.tree = tree
        self.displayed_tree = Canvas(self, width = 9 * WIDTH, height = 20 * WIDTH)
        self.displayed_tree.grid()
        scrollbar = Scrollbar(self, orient = VERTICAL, command = self.displayed_tree.yview)
        self.displayed_tree.config(yscrollcommand = scrollbar.set)
        scrollbar.grid(row = 0, column = 1, sticky = NS)
        self.displayed_tree.bind('<1>', lambda event, expand = True : self.expand_or_collapse_tree(event, expand))
        self.displayed_tree.bind('<Control-1>', lambda event, expand = False : self.expand_or_collapse_tree(event, expand))
        self.display_state(0, self.tree)        
        
    def display_search_tree(self, tree):
        if tree.displayed:       
            self.display_state(self.current_line, tree)
            self.current_line += 1
            for subtree in tree.next_states:
                self.display_search_tree(subtree)

    def display_state(self, line, tree):
        tree.display_state(self.displayed_tree, line)

    def expand_or_collapse_tree(self, event, expand):
        states = [self.tree]
        found_state = None
        while states:
            state = states.pop()
            if state.displayed and state.x < self.displayed_tree.canvasx(event.x) < state.x + WIDTH and\
               state.y < self.displayed_tree.canvasy(event.y) < state.y + WIDTH:
                found_state = state
                break
            states.extend(state.next_states)
        if found_state:
            if expand:
                for subtree in found_state.next_states:
                    subtree.displayed = True
            else:
                for subtree in found_state.next_states:
                    self.cancel_display(subtree)
            self.displayed_tree.delete(ALL)
            height = self.number_of_states_to_display(self.tree)
            self.displayed_tree.config(scrollregion = (0, 0, 9 * WIDTH, (height + 1) * WIDTH))
            self.current_line = 0
            self.display_search_tree(self.tree)
               
    def number_of_states_to_display(self, tree):
        if tree.displayed:
            return 1 + sum([self.number_of_states_to_display(subtree) for subtree in tree.next_states])
        return 0

    def cancel_display(self, tree):
        if tree.displayed:
            tree.displayed = False
            for subtree in tree.next_states:
                self.cancel_display(subtree)

class Game:
    def __init__(self, search_tree):
        self.search_tree = deepcopy(search_tree)

    def learn(self, displayed_games = None, game_nb = None):
        return self.play(self.search_tree, None, RED, displayed_games, game_nb)

    def play(self, current_state, previous_state, depth, displayed_games, game_nb):
        if depth % 2:
            if not current_state.next_states:
                return BLACK
            next_state = current_state.next_states[randrange(len(current_state.next_states))]
            next_state.depth = depth
            if displayed_games:
                next_state.display_state(displayed_games, game_nb)
            if not next_state.next_states:
                for tree in self.search_tree.next_states:
                    self.remove_state_from_possible_states(tree, current_state, previous_state)
                return RED
            return self.play(next_state, None, depth + 1, displayed_games, game_nb)
        next_state = current_state.next_states[randrange(len(current_state.next_states))]
        next_state.depth = depth
        if displayed_games:
            next_state.display_state(displayed_games, game_nb)
        return self.play(next_state, current_state, depth + 1, displayed_games, game_nb)

    def remove_state_from_possible_states(self, tree, current_state, previous_state):
        for subtree in tree.next_states:
            if subtree.code == current_state.code:
                tree.next_states.remove(subtree)
                break
        for subtree in tree.next_states:
            for subsubtree in subtree.next_states:
                self.remove_state_from_possible_states(subsubtree, current_state, previous_state)
                    
    def prune(self, tree):
        if any(subtree.expected_outcome != ON_TRACK_TO_LOSE for subtree in tree.next_states):
            for subtree in tree.next_states:
                if subtree.expected_outcome == ON_TRACK_TO_LOSE:
                    tree.next_states.remove(subtree)
        for subtree in tree.next_states:
            for subsubtree in subtree.next_states:
                self.prune(subsubtree)
               
    def well_pruned(self, tree):
        if tree.expected_outcome != ON_TRACK_TO_WIN:
           return False
        for subtree in tree.next_states:
            for subsubtree in subtree.next_states:
                if not self.well_pruned(subsubtree):
                    return False
        return True


class SimulationBoard(Frame):
    def __init__(self, search_tree):
        Frame.__init__(self, padx = 20, pady = 20)
        self.search_tree = search_tree
        opponent_button = Menubutton(self, text = 'Opponent', pady = 20)
        opponent_button.grid()
        players = Menu(opponent_button)
        players.add_command(label = 'Random player', command = lambda random_player = True : self.learn(random_player))
        players.add_command(label = 'Good player', command = lambda random_player = False : self.learn(random_player))
        opponent_button.config(menu = players)
        self.displayed_games = Canvas(self, width = 9 * WIDTH, height = 20 * WIDTH)
        self.displayed_games.grid()
        self.displayed_wins = Canvas(self, width = 250, height = 500)
        self.displayed_wins.grid(row = 1, column = 2)
        
    def learn(self, random_player):
        black_wins = [None] * 100
        self.displayed_games.delete(ALL)
        self.game = Game(self.search_tree)
        if not random_player:
            self.game.prune(self.game.search_tree)
        learning_over = False
        for i in range(19):
            black_wins[i] = self.game.learn(self.displayed_games, i)
            if not learning_over and self.game.well_pruned(self.game.search_tree):
                learning_over = i + 1
        for i in range(19, 100):
            black_wins[i] = self.game.learn()
            if not learning_over and self.game.well_pruned(self.game.search_tree):
                learning_over = i + 1
        self.displayed_wins.delete(ALL)
        self.displayed_wins.create_line(5, 250, 205, 250, fill = 'yellow')
        y = 0
        for x in range(100):
            if black_wins[x] == BLACK:
                self.displayed_wins.create_line(2 * x + 5, y + 250, 2 * x + 7, y + 248)
                y -= 2
            else:
                self.displayed_wins.create_line(2 * x + 5, y + 250, 2 * x + 7, y + 252)
                y += 2
        if random_player:
            self.displayed_wins.create_text(100, 17, text = 'Results with random player\nover 100 games')
        else:
            self.displayed_wins.create_text(100, 17, text = 'Results with good player\nover 100 games')
        if learning_over:
            self.displayed_wins.create_text(125, 445, text = 'Learning was completed after {} games'.format(learning_over))
        else:
            for i in range(100, 1000):
                self.game.learn()
                if self.game.well_pruned(self.game.search_tree):
                    self.displayed_wins.create_text(125, 445, text = 'No more to learn after {} games'.format(i + 1))
                    learning_over = True
                    break
            if not learning_over:
                self.displayed_wins.create_text(125, 445, text = '1000 games over, and more to learn...')


if __name__ == '__main__':
    WinningStrategy().mainloop()

    
        
