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

    def drawCard(self, amount, uno):
        self.cards_needed = amount
        for i in range(amount):
            if uno.deck.deck:
                new_card = random.choice(uno.deck.deck)
                uno.deck.deck.remove(new_card)
                self.cards.append(new_card)
                self.cards_needed -= 1
        if not uno.deck.deck:
            uno.shuffleDeck()
            self.drawCard(self.cards_needed, uno)

            
