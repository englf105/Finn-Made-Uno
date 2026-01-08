from card import Card
import random

class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in (self.cards):
                rep += str(card) + ", "
        else:
            rep = "<empty>"
        return rep

    def drawCard(self, amount, deck, uno):
        while deck:
            for i in range(amount):
                new_card = random.choice(deck.deck)
                deck.deck.remove(new_card)
                self.cards.append(new_card)
            
