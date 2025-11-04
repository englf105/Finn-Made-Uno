import card

class Hand:
    
    player_cards = []
    display_cards = []

    def DrawCard(amount):
        for i in range(amount):
            new_card = card.Card.randomCard()
            Hand.player_cards.append(new_card)
            Hand.display_cards.append(("_").join(new_card))
