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
        while (self.game_card.number == "skip" or self.game_card.number == "reverse" or self.game_card.number == "plus" or self.game_card.color == "wild"):
            self.game_card = card.Card.randomCard()

    def checkPlayerAmount(self):
        while (self.player_amount > 3 or self.player_amount < 1):
            self.player_amount = int(input("Enter amount of players (2-4): ")) - 1
            if (self.player_amount > 3 or self.player_amount < 1):
                print("\n///// Invalid amount of players /////\n")

    def displayTurnInfo(self, players):
        """ Diplaying turn info in the console"""
        if (self.turn == 0): 
            print(f"\n\033[33m===== Your turn =====\033[0m")
        else: 
            print(f"\n\033[33m===== Player {self.turn + 1} turn =====\033[0m")
        print(f"Current card: {self.game_card.color}_{self.game_card.number}")
        print(players[self.turn])

    def placeCard(self, cards, card_num):
        self.game_card.color = cards[card_num].color # Card Color
        self.game_card.number = cards[card_num].number # Card Number
        del cards[card_num] # Removing from the actual hand
    
    def checkEffect(self, players):
        if (self.game_card.number == "plus"):
            plus_turn = self.turn
            plus_turn += self.order_multiplier
            if (plus_turn > self.player_amount): # If the turn goes over # of players
                plus_turn = 0 
            if (plus_turn) < 0: # If the turn goes under 0
                plus_turn = self.player_amount 

            players[plus_turn].hand.drawCard(2)
            if (plus_turn == 0): 
                print(f"\n===== You drew two cards! =====")
            else: 
                print(f"\n===== Player {plus_turn + 1} drew two cards! =====")
        
        if (self.game_card.number == "choose"):
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
                    self.game_card.color = players[self.turn].hand.cards[wild].color
                    wild += 1
                    if wild > len(players[self.turn].hand.cards):
                        self.game_card.color = random.choice(card.Card.color)
            self.game_card.number = "<any>"
            print(f"\n===== Color has been changed to {self.game_card.color}! =====")

        if (self.game_card.number == "reverse"):
            self.order_multiplier = self.order_multiplier * -1
            print("\n===== The turns are reversed! =====")

        if (self.game_card.number == "skip"):
            self.turn += (1 * self.order_multiplier)
            if (self.turn > self.player_amount): 
                self.turn = 0
            if (self.turn) < 0: 
                self.turn = self.player_amount
            print("\n===== A turn was skipped! =====") 

    def nextTurn(self):
        self.turn += (1 * self.order_multiplier)
        if (self.turn > self.player_amount): # If the turn goes over # of players
            self.turn = 0
        if (self.turn) < 0: # If the turn goes under 0
            self.turn = self.player_amount
