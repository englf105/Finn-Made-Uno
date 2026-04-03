import random
from card import Card


class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        self.cards.sort(key=lambda s: (Card.color.index(s.color), s.number))
        if self.cards:
            rep = ""
            for card in (self.cards):
                rep += str(card) + ", "
        else: rep = "<empty>"
        return rep

    def displayHand(self, display_card, player):
        self.cards.sort(key=lambda s: (Card.color.index(s.color), s.number))
        if self.cards:
            rep = ""
            for card in (self.cards):
                if (((display_card.color == card.color or 
                      card.color == "wild") or 
                     display_card.number == card.number) and player):
                    rep += "\033[33m"
                rep += f"({self.cards.index(card) + 1}) "
                rep += str(card) + "\033[0m, "
        else: rep = "<empty>"
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
            if len(uno.discards) > 1:
                uno.shuffleDeck()
                self.drawCard(cards_needed, uno)
            else:
                print("\n\033[34m===== There are no cards " + 
                      "left in the deck! =====\033[0m")
