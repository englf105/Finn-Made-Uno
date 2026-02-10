from deck import Deck
from player import Player
from player_ai import Ai
from card import Card
import random
import copy


class Game():

    def __init__(self):
        self.deck = Deck()
        self.order_multiplier = 1
        self.player_amount = 0 
        self.turn = 0
        self.discards = []
        self.display_card = ""

        print(f"\033[33m===== Welcome to Uno! =====\033[0m")    
        self.setRandomCard()
        self.checkPlayerAmount()   

    def setRandomCard(self):
        forbidden_cards = ["skip", "reverse", "plus", "card", "plus_4"]
        self.discards.append(self.deck.getRandomCard())
        if self.discards[-1].number in forbidden_cards:
            while self.discards[-1].number in forbidden_cards:
                self.discards.append(self.deck.getRandomCard())
        self.display_card = copy.deepcopy(self.discards[-1])

    def checkPlayerAmount(self):
        while self.player_amount > 5 or self.player_amount < 1:
            self.player_amount = int(input("Enter total amount of players (2-6): ")) - 1
            if self.player_amount > 5 or self.player_amount < 1:
                print("\n///// Invalid  amount of players /////\n")

    def addPlayers(self, players, uno):
        players.append(Player(uno)) # Adds player to first player slot
        for i in range(self.player_amount):
            players.append(Ai(uno))

    def displayTurnInfo(self, players):
        print(f"\n\033[33m===== {self.displayName(self.turn, True)} turn =====\033[0m")
        print(f"Current card: {self.display_card}")
        print(players[self.turn].displayHand(self.display_card))

    def displayName(self, turn, possesive):
        if turn == 0 and possesive: return "Your"
        elif turn == 0 and not possesive: return "You"
        else: return f"Player {turn + 1}"

    def playerTurn(self, players, uno):
        if isinstance(players[self.turn], Player): # During player's turn
            players[self.turn].playerTurn(uno, players)
        elif isinstance(players[uno.turn], Ai): # During AI's turn
            players[self.turn].botTurn(uno, players)

    def placeCard(self, cards, card_num):
        self.discards.append(cards[card_num]) # Putting card into discard pile
        self.display_card = copy.deepcopy(cards[card_num])
        cards.pop(card_num) # Removing the card from hand
    
    def checkEffect(self, players, uno):
        self.checkWild(players, uno)
        self.checkPlus(players, uno)
        self.checkReverse()
        self.checkSkip()
        
    def checkWild(self, players, uno):
        if self.display_card.color == "wild":
            if isinstance(players[self.turn], Player):
                color = input("Enter color you wish to change to (r/y/g/b): ")
                for item in Card.color:
                    if color == item[0]:
                        self.display_card.color = item
            elif isinstance(players[self.turn], Ai):
                for card in players[self.turn].hand.cards:
                    if card.color != "wild":
                        self.display_card.color = card.color
                        break
                if self.display_card.color == "wild":
                        self.display_card.color = random.choice(Card.color)
            if self.display_card.number == "plus_4":
                plus_turn = self.turn + self.order_multiplier
                plus_turn = self.turnLimit(plus_turn, self.player_amount)
                players[plus_turn].hand.drawCard(4, uno)
                print(f"\n===== {self.displayName(plus_turn, False)} drew four cards! =====")
                self.turn += self.order_multiplier
                self.turn = self.turnLimit(self.turn, self.player_amount)
            self.display_card.number = "<any>"
            print(f"\n===== Color has been changed to {self.display_card.color}! =====")

    def checkPlus(self, players, uno):
        if self.display_card.number == "plus":
            plus_turn = self.turn + self.order_multiplier
            plus_turn = self.turnLimit(plus_turn, self.player_amount)
            players[plus_turn].hand.drawCard(2, uno)
            print(f"\n===== {self.displayName(plus_turn, False)} drew two cards! =====")
            self.turn += self.order_multiplier
            self.turn = self.turnLimit(self.turn, self.player_amount)

    def checkReverse(self):
        if self.display_card.number == "reverse":
            self.order_multiplier = self.order_multiplier * -1
            print("\n===== The turns are reversed! =====")

    def checkSkip(self):
        if self.display_card.number == "skip":
            self.turn += self.order_multiplier
            self.turn = self.turnLimit(self.turn, self.player_amount)
            print("\n===== A turn was skipped! =====") 

    def turnLimit(self, turn, limit):
        if turn > limit: return 0 # If the turn goes over # of players
        elif turn < 0: return limit # If the turn goes under 0
        else: return turn # If no conditions apply
        
    def nextTurn(self):
        self.turn += self.order_multiplier
        self.turn = self.turnLimit(self.turn, self.player_amount)

    def shuffleDeck(self):
        if not self.deck.deck:
            print("\n\033[34m===== A the deck has been shuffled! =====\033[0m")
            self.deck.deck = self.discards[:-1] # Sets deck to cards in discards except most recent
            self.discards = self.discards[-1:] # Removes all cards in discards except most recent