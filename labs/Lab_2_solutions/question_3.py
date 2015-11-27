# Simulates the cast of an unknown die, chosen from a set of 5 dice with
# 4, 6, 8, 12, and 20 sides.
# To start with, every die has a probability of 0.2 to be the chosen die.
# At every cast, the probability of each die is updated using Bayes' rule.
# The probabilities are displayed for at most 6 casts.
# If more than 6 casts have been requested,
# the final probabilities obtained for the chosen number of casts
# are eventually displayed.
#
# Written by Eric Martin for COMP9021


from random import choice, randint


NB_OF_SIMULATIONS_TO_DISPLAY = 5


nb_of_dice = 5
nb_of_possible_outcomes = 20
nb_of_faces = [4, 6, 8, 12, 20]
hypotheses_probabilities = [0.2] * nb_of_dice
outcomes_probabilities = [None] * nb_of_possible_outcomes

while True:
    try:
        nb_of_casts = int(input('Enter the desired number of times a randomly chosen die will be cast: '))
        break
    except:
        pass

chosen_nb_of_faces = choice(nb_of_faces)
print('\nThis is a secret, but the chosen die is the one with {:} faces\n'.format(chosen_nb_of_faces))
for cast in range(nb_of_casts):
    for possible_outcome in range(nb_of_possible_outcomes):
        outcomes_probabilities[possible_outcome] = 0
        # Let H_1, ..., H_5 be the hypotheses that the chosen die has 4, 6, 8, 12, 20 sides, respectively.
        # Let D be the hypothesis that the last cast yield n for a particular number n between 1 and the number of sides of the chosen die.
        # Then, denoting by p the probability function, p(D) = p(D/H_1)p(H_1) + ... + p(D/H_5)p(H_5)
        # where p(D/H_i) == 0 in case n is greater than the number of sides of the die associated with H_i.
        for die in range(nb_of_dice):
            if possible_outcome < nb_of_faces[die]:
                outcomes_probabilities[possible_outcome] += hypotheses_probabilities[die] / nb_of_faces[die]
    number_cast = choice(range(chosen_nb_of_faces))
    for die in range(nb_of_dice):
        if number_cast >= nb_of_faces[die]:           
            hypotheses_probabilities[die] = 0
        else:
            # The old value of hypotheses_probabilities[die] is the prior -- p(H_i) --, and
            # the new value of hypotheses_probabilities[die] is the posterior -- p(H_i/D) --.
            # We apply Bayes rule: p(H_i/D) = p(D/H_i) * p(H_i) / p(D)
            # with p(D/H_i) = 1 / nb_of_faces[die]
            #      p(H_i) = hypotheses_probabilities[die]
            #      p(D) = outcomes_probabilities[number_cast]
            hypotheses_probabilities[die] = hypotheses_probabilities[die] / (nb_of_faces[die] * outcomes_probabilities[number_cast])
    if cast < NB_OF_SIMULATIONS_TO_DISPLAY:
        print('The die that has been cast yields: {:}'.format(number_cast + 1))
        print('The updated dice probabilies are:')
        for die in range(nb_of_dice):
            print('\t{:2d}: {:.2f}%'.format(nb_of_faces[die], hypotheses_probabilities[die] * 100))
        print()
if nb_of_casts > NB_OF_SIMULATIONS_TO_DISPLAY:
    print('The final probabilities are:')             
    for die in range(nb_of_dice):
        print('\t{:2d}: {:.2f}%'.format(nb_of_faces[die], hypotheses_probabilities[die] * 100))
        
    
    
