from card import Card

class Deck:

    def __init__(self):
        self.deck_cards = []
        for item in (Card.color not in "wild"):
            for item in Card.number:
                self.deck_cards.append(Card(Card.color, Card.number))

    def __str__(self):
        if self.cards:
            rep = ""
            for card in (self.cards):
                rep += str(card) + ", "
        else:
            rep = "<empty>"
        return rep

    def drawCard(self, amount):
        for i in range(amount):
            new_card = Card.randomCard()
            self.cards.append(new_card)