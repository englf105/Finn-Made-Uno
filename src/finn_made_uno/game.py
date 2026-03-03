from deck import Deck
from player import Player
from player_ai import Ai
from card import Card
from num2words import num2words
import random
import copy


class Game():

    def __init__(self):
        self.deck = Deck()
        self.order_multiplier = 1
        self.player_amount = 0 
        self.players = []
        self.turn = 0
        self.discards = []
        self.display_card = ""
        self.stack = 0

        """ Settings """
        self.place_after_draw = False
        self.draw_till_place = False
        self.stack_plus_cards = False
        
        print(f"\033[33m===== Welcome to Uno! =====\033[0m")    
        self.setStartingCard()
        self.setPlayerAmount()   

    def setStartingCard(self):
        forbidden_cards = ["skip", "reverse", "plus", "card", "plus_4"]
        self.discards.append(self.deck.getRandomCard())
        if self.discards[-1].number in forbidden_cards:
            while self.discards[-1].number in forbidden_cards:
                self.discards.append(self.deck.getRandomCard())
        self.display_card = copy.deepcopy(self.discards[-1])

    def setPlayerAmount(self):
        while self.player_amount > 5 or self.player_amount < 1:
            self.player_amount = int(input("Enter total amount of players (2-6): ")) - 1
            if self.player_amount > 5 or self.player_amount < 1:
                print("\n///// Invalid  amount of players /////\n")
        self.players.append(Player(self)) # Adds player to first player slot
        for i in range(self.player_amount):
            self.players.append(Ai(self)) # Adds the amount of Ai inputted

    def playerHasCards(self):
        for player in self.players:
            if len(player.hand.cards) == 0:
                return False # Stops if player has no cards
        return True # Keeps game going if all players have cards

    def displayTurnInfo(self):
        print(f"\n\033[33m===== {self.displayName(self.turn, True)} turn =====\033[0m")
        print(f"Current card: {self.display_card}")
        print(self.players[self.turn].displayHand(self.display_card))

    def displayName(self, turn, possesive):
        if turn == 0 and possesive: return "Your"
        elif turn == 0 and not possesive: return "You"
        else: return f"Player {turn + 1}"

    def playerTurn(self):
        if isinstance(self.players[self.turn], Player): # During player's turn
            self.players[self.turn].playerTurn(self, self.players)
        elif isinstance(self.players[self.turn], Ai): # During AI's turn
            self.players[self.turn].botTurn(self, self.players)

    def placeCard(self, cards, card):
        self.discards.append(card) # Putting card into discard pile
        self.display_card = copy.deepcopy(card)
        cards.remove(card) # Removing the card from hand
    
    def checkEffect(self):
        self.checkWild()
        self.checkPlus()
        self.checkReverse()
        self.checkSkip()
        
    def checkWild(self):
        if self.display_card.color == "wild":
            if isinstance(self.players[self.turn], Player):
                color = ""
                colors = ["r", "y", "g", "b"]
                while color not in colors:
                    color = input("Enter color you wish to change to (r/y/g/b): ")
                for item in Card.color:
                    if color == item[0]:
                        self.display_card.color = item
            elif isinstance(self.players[self.turn], Ai):
                for card in self.players[self.turn].hand.cards:
                    if card.color != "wild":
                        self.display_card.color = card.color
                        break
                if self.display_card.color == "wild":
                    self.display_card.color = random.choice(Card.color[:4])
            if self.display_card.number == "plus_4":
                plus_turn = self.turn + self.order_multiplier
                plus_turn = self.turnLimit(plus_turn, self.player_amount)
                self.players[plus_turn].hand.drawCard(4, self)
                print(f"\n===== {self.displayName(plus_turn, False)} drew four cards! =====")
                self.nextTurn()
            self.display_card.number = "<any>"
            print(f"\n===== Color has been changed to {self.display_card.color}! =====")

    def checkPlus(self):
        if self.display_card.number == "plus":

            # Find next player to add cards to
            next_turn = self.turn + self.order_multiplier
            next_turn = self.turnLimit(next_turn, self.player_amount)     

            # Searches next player hand to see if they have a plus
            if self.stack_plus_cards:
                for card in self.players[next_turn].hand.cards:
                    if card.number == "plus":
                        self.stack += 1

            # Give them the amount of cards needed
            if self.stack == 0:
                self.players[next_turn].hand.drawCard(2, self)
                print(f"\n===== {self.displayName(next_turn, False)} drew two cards! =====")

            # Go to next turn
            self.turn += self.order_multiplier
            self.turn = self.turnLimit(self.turn, self.player_amount)
        
        # If the plus stack is greater than 0 and no plus card is placed
        elif self.stack > 0:  

                # Give the current player that many cards
                self.players[self.turn].hand.drawCard(self.stack * 2, self)
                print(f"\n===== {self.displayName(self.turn, False)} drew {num2words(self.stack * 2)} cards! =====")
                self.stack = 0

    def checkReverse(self):
        if self.display_card.number == "reverse":
            if self.player_amount > 1:
                self.order_multiplier = self.order_multiplier * -1
                print("\n===== The turns are reversed! =====")
            else: 
                print(f"\n===== The turn goes back to {self.displayName(self.turn, False)}! =====")
                self.nextTurn()

    def checkSkip(self):
        if self.display_card.number == "skip":
            self.nextTurn()
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
        
    def validCard(self, card):
        same_color = self.display_card.color == card.color 
        same_number = self.display_card.number == card.number
        is_wild = card.color == "wild"
        if same_color or same_number or is_wild: return True
        else: return False
    
    def winnerMessage(self):
        for player in self.players:
            if len(player.hand.cards) == 0:
                winner = self.players.index(player) + 1
                return f"\n\033[34m===== Player {winner} won Uno! =====\033[0m\n"