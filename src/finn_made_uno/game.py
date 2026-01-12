from card import Card
import random
from player import Player
from player_ai import Ai

class Game():

    def __init__(self, deck):
        self.order_multiplier = 1
        self.player_amount = 0
        self.turn = 0
        self.discards = []
        self.times_shuffled = 0

        print(f"\033[33m===== Welcome to Uno! =====\033[0m")    
        self.setRandomCard(deck)
        self.checkPlayerAmount()   

    def setRandomCard(self, deck):
        self.discards.append(deck.getRandomCard())
        forbidden_cards = ["skip", "reverse", "plus", "wild"]
        while (self.discards[-1].number not in forbidden_cards):
            self.discards.append(deck.getRandomCard())

    def checkPlayerAmount(self):
        self.player_amount = 3
        """
        while (self.player_amount > 3 or self.player_amount < 1):
            self.player_amount = int(input("Enter amount of players (2-4): ")) - 1
            if (self.player_amount > 3 or self.player_amount < 1):
                print("\n///// Invalid  amount of players /////\n")
                """

    def displayTurnInfo(self, players):
        print(f"\n\033[33m===== {self.displayName(self.turn, True)} turn =====\033[0m")
        print(f"Current card: {self.discards[-1]}")
        print(players[self.turn])

    def placeCard(self, cards, card_num):
        self.discards.append(cards[card_num]) # Putting card into discard pile
        del cards[card_num] # Removing the card from hand
    
    def checkEffect(self, players, deck, uno):
        self.checkWild(players, deck, uno)
        self.checkPlus(players, deck, uno)
        self.checkReverse()
        self.checkSkip()
        
    def checkWild(self, players, deck, uno):
        if (self.discards[-1].color == "wild"):
            if isinstance(players[self.turn], Player):
                color = input("Enter color you wish to change to (r/y/g/b): ")
                if color == "r": 
                    self.discards[-1].color = "red"
                elif color == "y":
                    self.discards[-1].color = "yellow"
                elif color == "g":
                    self.discards[-1].color = "green"
                elif color == "b":
                    self.discards[-1].color = "blue"
            elif isinstance(players[self.turn], Ai):
                wild = 0
                while self.discards[-1].color == "wild":
                    if len(players[self.turn].hand.cards) > 0:
                        if players[self.turn].hand.cards[wild].color != "wild":
                            self.discards[-1].color = players[self.turn].hand.cards[wild].color
                    else:
                        break
                    wild += 1
                    if wild > len(players[self.turn].hand.cards):
                        self.discards[-1].color = random.choice(Card.color)
            if self.discards[-1].number == "plus_4":
                plus_turn = self.turn
                plus_turn += self.order_multiplier
                plus_turn = self.turnLimit(plus_turn, self.player_amount)
                players[plus_turn].hand.drawCard(4, deck, uno)
                print(f"\n===== {self.displayName(plus_turn, False)} drew four cards! =====")
            self.discards[-1].number = "<any>"
            print(f"\n===== Color has been changed to {self.discards[-1].color}! =====")

    def checkPlus(self, players, deck, uno):
        if (self.discards[-1].number == "plus"):
            plus_turn = self.turn
            plus_turn += self.order_multiplier
            plus_turn = self.turnLimit(plus_turn, self.player_amount)
            players[plus_turn].hand.drawCard(2, deck, uno)
            print(f"\n===== {self.displayName(plus_turn, False)} drew two cards! =====")

    def checkReverse(self):
        if (self.discards[-1].number == "reverse"):
            self.order_multiplier = self.order_multiplier * -1
            print("\n===== The turns are reversed! =====")

    def checkSkip(self):
        if (self.discards[-1].number == "skip"):
            self.turn += (self.order_multiplier)
            self.turn = self.turnLimit(self.turn, self.player_amount)
            print("\n===== A turn was skipped! =====") 

    def displayName(self, turn, possesive):
        if (turn == 0): 
            if possesive == True:
                return "Your"
            else:
                return "You"
        else: 
            return f"Player {turn + 1}"

    def turnLimit(self, turn, limit):
        if (turn > limit): # If the turn goes over # of players
            return 0
        elif (turn) < 0: # If the turn goes under 0
            return limit
        else: # If no conditions apply
            return turn
        
    def nextTurn(self):
        self.turn += (1 * self.order_multiplier)
        self.turn = self.turnLimit(self.turn, self.player_amount)

    def shuffleDeck(self, deck):
        if not deck.deck:
            print("\n===== A the deck has been shuffled! =====")
            deck.deck = self.discards[:-1]
            self.discards = self.discards[-1:]
            self.times_shuffled += 1
        else:
            self.shuffleDeck(deck)



