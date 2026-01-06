from card import Card

class Deck:

    def __init__(self):
        self.deck = []
        for i in range(2): self.deck.extend([Card(color, number) for color in Card.color[0:4] for number in Card.number[1:13]])
        self.deck.extend([Card(color, number) for color in Card.color[0:4] for number in Card.number[0]])
        for i in range(4): self.deck.extend([Card(Card.color[4], number) for number in Card.wild_types])
        self.deck.sort(key=lambda s: (Card.color.index(s.color), s.number))
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