from card import Card

class Deck:

    def __init__(self):
        self.deck = [Card(color, number) for color in Card.color in deck if Card.color != "wild" for number in Card.number]
        self.discards = []

    def __str__(self):
        if self.deck:
            rep = ""
            for card in (self.deck):
                rep += str(card) + ", "
        else:
            rep = "<empty>"
        return rep

    def drawCard(self, amount):
        for i in range(amount):
            new_card = Card.randomCard()
            self.deck.append(new_card)

if __name__ == "__main__":
    deck = Deck()
    print(deck)