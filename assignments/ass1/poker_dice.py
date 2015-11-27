# Write a program named poker_dice.py that simulates the roll of 5 dice, at most
# three times, as described at http://en.wikipedia.org/wiki/Poker_dice as well
# as a given number of rolls of the 5 dice to evaluate the probabilies of the
# various hands.

from random import randint

aList = ["Ace","King","Queen", "Jack", "10", "9"]

# Generates a list L randomly between 0 to 5 that appends the values of aList
# to it:

def generate_list():
  L = []
  nb_of_dice = 5
  for i in range(nb_of_dice):
    DiceIndex = randint(0,5)
    L.append(aList[DiceIndex])
    L.sort(reverse = True)
  return L

# Return results using a dictionary to count maximum times an element appears
# and the measuring the length of a list without duplicates to return results:

def results(L):
  aDict = {}
  for element in L:
    if element not in aDict:
      aDict[element] = 1
    else:
      aDict[element] += 1

  if len(set(L)) == 1:
    return 'Five'
  
  elif len(set(L)) == 2:
    if max(aDict.values()) == 4:
      return 'Four'
    else:
      return 'Full House'
    
  elif len(set(L)) == 5:
    if 'Ace' in L and '9' in L:
      return 'Bust'
    else:
      if L == ['Ace', 'King', 'Queen', 'Jack', '10'] or L == ['King', 'Queen', 'Jack', '10', '9']:
        return 'Straight'
      else:
        return 'Bust'
    
  elif len(set(L)) == 3:
    if max(aDict.values()) == 3:
      return 'Three'
    else:
      return 'Two Pair'
    
  elif len(set(L)) == 4:
    return 'One Pair'
    
  return results

def play():
    L = generate_list()
    a = results(L)

    print('The roll is:', ' '.join(L))
    
    if a=='One Pair':
      print("It is a One pair")
    elif a=='Two Pair':
       print("It is a Two pair")
    elif a=='Three':
      print("It is Three of a kind")
    elif a=='Four':
      print("It is a Four of a kind")
    elif a=='Five':
      print("It is a Five of a kind")
    elif a == 'Full House':
      print("It is a Full House")
    elif a == 'Straight':
      print("It is a Straight")
    elif a == 'Bust':
      print("It is a Bust")
      
