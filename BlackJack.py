# Simulate a simplified version of BlackJack


import random
import time

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

class Card():

  def __init__(self,suit,rank):
    self.suit = suit
    self.rank = rank
    self.value = values[rank]

  def __str__(self):
    return self.rank + " of " + self.suit

class Deck():

  def __init__(self):

    self.all_cards = []

    for suit in suits:
      for rank in ranks:
        created_card = Card(suit,rank)
        self.all_cards.append(created_card)

  def shuffle(self):

    random.shuffle(self.all_cards)

  def deal_one(self):
    return self.all_cards.pop()

class Player():

  def __init__(self,name,chips):

    self.name = name
    self.all_cards = [] # a players current hand
    self.chips = int(chips)

  def remove_one(self):
    return self.all_cards.pop(0)

  def add_cards(self,new_cards):
    if type(new_cards) == type([]):
      self.all_cards.extend(new_cards)
    else:
      self.all_cards.append(new_cards)

  def __str__(self):
    return "{} has {} cards".format(self.name,len(self.all_cards))


def hand_value(player,hand):
  hand_value = 0
  cards = []
  for card in hand:
    hand_value = hand_value + card.value
    cards.append(str(card))
  print("\t{}'s hand value: {} ({})".format(player, hand_value, cards))
  return hand_value


# game setup, initialize some variables
player_one = Player("Player 1", 100) # name and chips
hand_player = []
hand_dealer = []
round_num = 1

# create deck of 52 cards sand shuffle
deck = Deck()
deck.shuffle()

game_on = True # main game boolean
dealer_turn = False # player vs dealer boolean

while game_on == True:

  # do we have enough cards?
  if len(deck.all_cards) == 0:
    game_on = False
    print('\nno more cards!')

  # does player one have enought chips
  elif player_one.chips == 0:
    game_on = False
    print("\nout of chips!")

  # all conditions met to start round, start with betting
  else:
    print("\n##### ROUND {} #####".format(round_num))

    # ask player for their bet, only accept bet if player has enough chips
    print("\nBETTING...")
    waiting_for_bet = True
    while waiting_for_bet:
      bet = input("{} please place your bet (you have {} chips): ".format(
          player_one.name, player_one.chips))
      try:
        bet = int(bet)
      except:
        print("\tplease enter a whole number")
      else:
        if bet > player_one.chips:
          print("you do not have enough chips, please place lower bet")
        else:
          print("your bet has been placed")
          waiting_for_bet = False

    print("\nDEALING CARDS...")
    hand_player.extend([deck.deal_one(), deck.deal_one()])
    hand_dealer.extend([deck.deal_one(), deck.deal_one()])

    #reveal players hand, and only 1 of dealer's cards
    hand_value(player_one.name, hand_player)
    print("\t{}'s card: {} ({})".format("dealer", hand_dealer[0].value, str(hand_dealer[0])))

    time.sleep(5)
    # main round while loop
    # exit criteria include player blackjack, player bust,
    # dealer blackjack, dealer bust, or highest value
    round_on = True
    while round_on == True:

      # player hit / stay loop
      print("\nPLAYERS'S TURN...")
      while dealer_turn == False:
        #check hand
        hand_value_player = hand_value(player_one.name,hand_player)

        # check for BLACKJACK or BUST, if none, move to hit/stay
        if hand_value_player == 21:
          print("\tBLACKJACK!!! {} is the Winner!".format(player_one.name))
          player_one.chips += bet
          round_on = False
          break
        if hand_value_player > 21:
          print("\tBUST! The Dealer is the Winner!")
          player_one.chips -= bet
          round_on = False
          break
        else:
          #ask the player if they wish to HIT or STAY
          hit_response = input("\treview the cards... type 'h' to HIT, or 's' to STAY\n")
          if hit_response == "h":
            # player chose to hit
            print("\tHit")
            hand_player.append(deck.deal_one())
          elif hit_response == "s":
            # player chose to stay
            print("\tStay")
            dealer_turn = True
            print("\nDEALERS'S TURN...")
          else:
            print("\tplease enter lowercase h or lowercase s")

      # dealer hit / stay loop
      while dealer_turn == True:

        # check dealer hand
        hand_value_dealer = hand_value("dealer",hand_dealer)

        # check for BLACKJACK or BUST, if none, move to hit/stay
        if hand_value_dealer == 21:
          print("\tDealer is the Winner!")
          player_one.chips -= bet
          round_on = False
          break
        elif hand_value_dealer > 21:
          print("\tBUST! The {} is the Winner!".format(player_one.name))
          player_one.chips += bet
          round_on = False
          break
        elif hand_value_player == hand_value_dealer:
          print("\tTie goes to the player?")
          player_one.chips += bet
          round_on = False
          break
        else:
          #dealer hits when <= 17
          if hand_value_dealer <= 17:
            hand_dealer.append(deck.deal_one())
          else:
            # winner handling
            if hand_value_player > hand_value_dealer:
              print("\t{} is the Winner!".format(player_one.name))
              player_one.chips += bet
              round_on = False
              break
            else:
              print("\t{} is the Winner!".format("dealer"))
              player_one.chips -= bet
              round_on = False
              break

    # index round number
    round_num += 1

    # reset the hands, and the turn variable
    hand_player = []
    hand_dealer = []
    dealer_turn = False

    # print round results
    print("\n{} now has {} chips".format(player_one.name, player_one.chips))

    time.sleep(5)

print("game over")
