import card

class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in (self.cards):
                rep += str(card)
        else:
            rep = "<empty>"
        return rep

    def drawCard(self, amount):
        for i in range(amount):
            new_card = card.Card.randomCard()
            self.cards.append(new_card)
