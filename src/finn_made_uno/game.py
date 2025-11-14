import card

class Game():
    
    player_amount = 1
    turn = 1
    game_card = ""

    def __init__(self):
        print(f"===== Welcome to Uno! =====")
        print(f"\nTurn: {Game.turn}")        

    def setRandomCard(self):
        self.game_card = card.Card.randomCard()
        while (self.game_card[1] == "skip" or self.game_card[1] == "reverse" or self.game_card[1] == "plus"):
            self.game_card = card.Card.randomCard()

    def checkPlayerAmount(self):
        while (self.player_amount > 4 or self.player_amount < 2):
            self.player_amount = int(input("\nEnter amount of players (2-4): "))
            if (self.player_amount > 4 or self.player_amount < 2):
                print("\n///// Invalid amount of players /////")
    
    def checkEffect(self, hand):
        if (self.game_card[1] == "plus"):
            hand.drawCard(2)
            print("\n===== Drew two more cards! =====")
        
        if (self.game_card[1] == "reverse"):
            order_multiplier = order_multiplier * -1
            print("\n===== The turns are reversed! =====")

        if (self.game_card[1] == "skip"):
            self.turn += (1 * order_multiplier)
            if (self.turn > self.player_amount):
                self.turn = 1
            if (self.turn) < 1:
                self.turn = self.player_amount
            print("\n===== A turn was skipped! =====")

    def placeCard(self, cards, card_num):
        """ Set the card placed to the current card """
        self.game_card[0] = cards[card_num][0] # Card Color
        self.game_card[1] = cards[card_num][1] # Card Number

        """ Delete the placed card from the hand """
        del cards[card_num] # Removing from the actual hand

    def nextTurn(self, order):
        self.turn += (1 * order)
        if (self.turn > self.player_amount): # If the turn goes over # of players
            self.turn = 1
        if (self.turn) < 1: # If the turn goes under 0
            self.turn = self.player_amount
