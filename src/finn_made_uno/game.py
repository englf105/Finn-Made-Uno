import card
import random
from player import Player
from player_ai import Ai

class Game():
    
    order_multiplier = 1
    player_amount = 0
    turn = 0
    game_card = ""

    def __init__(self):
        print(f"\033[33m===== Welcome to Uno! =====\033[0m")    
        self.setRandomCard()
        self.checkPlayerAmount()   

    def setRandomCard(self):
        self.game_card = card.Card.randomCard()
        forbidden_cards = ["skip", "reverse", "plus", "wild"]
        while (self.game_card.number not in forbidden_cards):
            self.game_card = card.Card.randomCard()

    def checkPlayerAmount(self):
        while (self.player_amount > 3 or self.player_amount < 1):
            self.player_amount = int(input("Enter amount of players (2-4): ")) - 1
            if (self.player_amount > 3 or self.player_amount < 1):
                print("\n///// Invalid  amount of players /////\n")

    def displayTurnInfo(self, players):
        print(f"\n\033[33m===== {self.displayName(self.turn, True)} turn =====\033[0m")
        print(f"Current card: {self.game_card}")
        print(players[self.turn])

    def placeCard(self, cards, card_num, deck):
        self.game_card = cards[card_num] # Card color
        deck.discards.append(card_num) # Putting card into discard pile
        cards.remove(card_num) # Removing the card from hand
    
    def checkEffect(self, players):
        self.checkWild(players)
        self.checkPlus(players)
        self.checkReverse()
        self.checkSkip()
        
    def checkWild(self, players):
        if (self.game_card.color == "wild"):
            if isinstance(players[self.turn], Player):
                color = input("Enter color you wish to change to (r/y/g/b): ")
                if color == "r": 
                    self.game_card.color = "red"
                elif color == "y":
                    self.game_card.color = "yellow"
                elif color == "g":
                    self.game_card.color = "green"
                elif color == "b":
                    self.game_card.color = "blue"
            elif isinstance(players[self.turn], Ai):
                wild = 0
                while self.game_card.color == "wild":
                    if len(players[self.turn].hand.cards) > 0:
                        self.game_card.color = players[self.turn].hand.cards[wild].color
                    else:
                        break
                    wild += 1
                    if wild > len(players[self.turn].hand.cards):
                        self.game_card.color = random.choice(card.Card.color)
            if self.game_card.number == "plus_4":
                plus_turn = self.turn
                plus_turn += self.order_multiplier
                plus_turn = self.turnLimit(plus_turn, self.player_amount)
                players[plus_turn].hand.drawCard(4)
                print(f"\n===== {self.displayName(plus_turn, False)} drew four cards! =====")
            self.game_card.number = "<any>"
            print(f"\n===== Color has been changed to {self.game_card.color}! =====")

    def checkPlus(self, players):
        if (self.game_card.number == "plus"):
            plus_turn = self.turn
            plus_turn += self.order_multiplier
            plus_turn = self.turnLimit(plus_turn, self.player_amount)
            players[plus_turn].hand.drawCard(2)
            print(f"\n===== {self.displayName(plus_turn, False)} drew two cards! =====")

    def checkReverse(self):
        if (self.game_card.number == "reverse"):
            self.order_multiplier = self.order_multiplier * -1
            print("\n===== The turns are reversed! =====")

    def checkSkip(self):
        if (self.game_card.number == "skip"):
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
