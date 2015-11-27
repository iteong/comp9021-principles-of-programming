# Simulates the Monty Hall problem.
# - A car is hidden behind 3 doors.
# - The contestant randomly choses a door.
# - The game host opens a door behind which there is no car.
# - The contestant then has the option to change his mind and open another door.
# Prompts the user for the number of times the game is played,
# and whether the contestants opts for swiching door or not.
# Simulates at most six games, and prints out the proportion of games being won.
#
# Written by Eric Martin for COMP9021


from random import choice


NB_OF_SIMULATIONS_TO_DISPLAY = 6


while True:
    try:
        nb_of_of_experiments = int(input('Enter the number of times the simulation should be run: '))
        if nb_of_of_experiments <= 0:
            raise Exception
        break
    except:
        pass
while True:
    try:
        contestant_switches = input('Do you want the contestant to switch door? ')
        if contestant_switches in {'Yes', 'yes', 'Y', 'y'}:
            contestant_switches = True
            break
        if contestant_switches in {'No', 'no', 'N', 'n'}:
            contestant_switches = False
            break
    except:
        pass
    
print('Starting the simulation with the contestant ', end = '')
if not contestant_switches:
    print('not ', end = '')
print('switching doors.\n')

nb_of_wins = 0
doors = ('A', 'B', 'C')
for i in range(nb_of_of_experiments):
    if i < NB_OF_SIMULATIONS_TO_DISPLAY:
        winning_door_index = choice([0, 1, 2])
        print('\tContestant does not know it, but car happens to be behind door {:}.'.format(doors[winning_door_index]))
    chosen_door_index = choice([0, 1, 2])
    if i < NB_OF_SIMULATIONS_TO_DISPLAY:
        print('\tContestant chooses door {:}.'.format(doors[chosen_door_index]))
    if chosen_door_index == winning_door_index:
        if chosen_door_index:
            remaining_indexes = [0, 3 - chosen_door_index]           
        else:
            remaining_indexes = [1, 2]
        opened_door_index = choice(remaining_indexes)
        if not contestant_switches:
            nb_of_wins += 1
    else:
        opened_door_index = 3 - winning_door_index - chosen_door_index
        if contestant_switches:
            nb_of_wins += 1            
    if i < NB_OF_SIMULATIONS_TO_DISPLAY:
        print('\tGame host opens door {:}.'.format(doors[opened_door_index]))
    if i < NB_OF_SIMULATIONS_TO_DISPLAY:
        if contestant_switches:
            print('\tContestant chooses door {:} and '.format(doors[3 - chosen_door_index - opened_door_index]), end = '')
        else:
            print('\tContestant chooses door {:} and '.format(doors[chosen_door_index]), end = '')
        if chosen_door_index == winning_door_index and not contestant_switches or chosen_door_index != winning_door_index and contestant_switches:
            print('wins.\n')
        else:
            print('looses.\n')            
    elif i == NB_OF_SIMULATIONS_TO_DISPLAY:
        print('...\n')
print('Contestant has won {:.2f}% of games.'.format(nb_of_wins / nb_of_of_experiments * 100))
            



