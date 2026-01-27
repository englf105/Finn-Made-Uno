from card import Card
import random

class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in (self.cards):
                rep += f"({self.cards.index(card) + 1}) "
                rep += str(card)
                rep +=", "
        else:
            rep = "<empty>"
        return rep

    def drawCard(self, amount, uno):
        cards_needed = amount
        deck = uno.deck.deck
        for i in range(amount):
            if deck:
                new_card = random.choice(deck)
                deck.remove(new_card)
                self.cards.append(new_card)
                cards_needed -= 1
        if not deck:
            uno.shuffleDeck()
            self.drawCard(cards_needed, uno)

            
