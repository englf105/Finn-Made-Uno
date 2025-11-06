import card

class Hand:
    
    player_cards = []

    def AiDrawCard(amount):
        for i in range(amount):
            new_card = card.Card.randomCard()
            Hand.player_cards.append(new_card)