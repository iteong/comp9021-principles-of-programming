# Written by Eric Martin for COMP9021


from tkinter import *
from random import randrange

BACKGROUND_COLOUR = '#D3D3D3'
DECK_SIZE = 52


class CardShuffling(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Card Shuffling Simulator')
        display = Frame(self, bd = 50)
        display.grid(column = 7)
        # self. is necessary to avoid that the variable be garbage collected after the class has been created
        self.card_images = [None] * DECK_SIZE
        self.cards_to_display = [None] * DECK_SIZE
        for i in range(DECK_SIZE):
            self.card_images[i] = PhotoImage(file = 'Cards/' + str(i + 1) + '.gif')
            self.cards_to_display[i] = Canvas(display, width = 74, height = 100, background = BACKGROUND_COLOUR)
        Button(display, text = 'Reset', command = self.reset).grid(row = 4, column = 4, pady = 40)
        Button(display, text = 'Shuffle', command = self.shuffle).grid(row = 4, column = 8)
        Label(display, text = 'Number of times the deck has been shuffled:').grid(row = 5, column = 5, columnspan = 4)
        self.shuffles = 0
        self.nb_of_times_shuffled = StringVar()
        self.nb_of_times_shuffled.set(0)
        Label(display, width = 2, height = 1, textvariable = self.nb_of_times_shuffled).grid(row = 5, column = 9)
        self.deck = [list(range(DECK_SIZE)), [None] * 52]
        self.switch = True
        self.reset()
            
    def reset(self):
        deck = self.deck[self.switch]
        for i in range(DECK_SIZE):
            deck[i] = i
        self.shuffles = 0
        self.nb_of_times_shuffled.set(0)
        self.display_deck()

    def shuffle(self):
        cut = 0
        for i in range(DECK_SIZE):
            cut += randrange(2)
        if i == 0 or i == DECK_SIZE:
            return
        stack_1_index = 0;
        stack_2_index = cut;
        both_stacks_size = DECK_SIZE;
        i = 0
        deck = self.deck[self.switch]
        new_deck = self.deck[not self.switch]
        while stack_1_index < cut and stack_2_index < DECK_SIZE:
            which_stack = randrange(both_stacks_size)
            both_stacks_size -= 1
            if which_stack < cut - stack_1_index:
                new_deck[i] = deck[stack_1_index]
                i += 1
                stack_1_index += 1
            else:
                new_deck[i] = deck[stack_2_index]
                i += 1
                stack_2_index += 1
        if stack_1_index < cut:
            for j in range(i, DECK_SIZE):
                new_deck[j] = deck[stack_1_index]
                stack_1_index += 1
        else:
            for j in range(i, DECK_SIZE):
                new_deck[j] = deck[stack_2_index]
                stack_2_index += 1
        self.switch = not self.switch
        self.shuffles += 1
        self.nb_of_times_shuffled.set(self.shuffles)
        self.display_deck()

    def display_deck(self):
        deck = self.deck[self.switch]
        for i in range(DECK_SIZE):
            self.cards_to_display[i].delete(ALL)
            self.cards_to_display[i].create_image(40, 53, image = self.card_images[deck[i]])
            self.cards_to_display[i].grid(row = i // 13, column = i % 13)
    
       
if __name__ == '__main__':
    CardShuffling().mainloop()

