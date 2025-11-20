import card

class Game():
    
    order_multiplier = 1
    player_amount = 1
    turn = 0
    game_card = ""

    def __init__(self):
        print(f"===== Welcome to Uno! =====")       

    def setRandomCard(self):
        self.game_card = card.Card.randomCard()
        while (self.game_card.number == "skip" or self.game_card.number == "reverse" or self.game_card.number == "plus"):
            self.game_card = card.Card.randomCard()

    def checkPlayerAmount(self):
        while (self.player_amount > 4 or self.player_amount < 2):
            self.player_amount = (int(input("Enter amount of players (2-4): ")) - 1)
            if (self.player_amount > 4 or self.player_amount < 2):
                print("\n///// Invalid amount of players /////")
    
    def checkEffect(self, hand, players):
        if (self.game_card.number == "plus"):

            if ((self.turn == 0) and (self.order_multiplier == -1)):
                players[len(players) - 1].hand.drawCard(2)
                print(f"\n===== Player {len(players)} drew two cards! =====")

            elif (self.turn == len(players) - 1) and (self.order_multiplier == 1):
                players[0].hand.drawCard(2)
                print(f"\n===== You drew two cards! =====")

            else:
                players[self.turn + (1 * self.order_multiplier)].hand.drawCard(2)
                print(f"\n===== Player {self.turn + (1 * self.order_multiplier)} drew two cards! =====")

        
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

    def placeCard(self, cards, card_num):
        """ Set the card placed to the current card """
        self.game_card.color = cards[card_num].color # Card Color
        self.game_card.number = cards[card_num].number # Card Number

        """ Delete the placed card from the hand """
        del cards[card_num] # Removing from the actual hand

    def nextTurn(self):
        self.turn += (1 * self.order_multiplier)
        if (self.turn > self.player_amount): # If the turn goes over # of players
            self.turn = 0
        if (self.turn) < 0: # If the turn goes under 0
            self.turn = self.player_amount
