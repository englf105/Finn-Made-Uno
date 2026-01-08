from card import Card
import random

class Deck:

    def __init__(self):
        self.deck = []
        for i in range(2): self.deck.extend([Card(color, number) for color in Card.color[0:4] for number in Card.number[1:13]])
        self.deck.extend([Card(color, number) for color in Card.color[0:4] for number in Card.number[0]])
        for i in range(4): self.deck.extend([Card(Card.color[4], number) for number in Card.wild_types])
        self.deck.sort(key=lambda s: (Card.color.index(s.color), s.number))

    def __str__(self, type):
        if type == "deck":
            if self.deck:
                rep = ""
                for card in (self.deck):
                    rep += str(card) + ", "
            else:
                rep = "<empty>"
            return rep

    def getRandomCard(self):
        new_card = random.choice(self.deck)
        self.deck.remove(new_card)
        return new_card

if __name__ == "__main__":
    deck = Deck()
    print(deck)