import hand

class Ai:
    
    def __init__(self, uno):
        self.hand = hand.Hand() # Creating the player's hand
        self.hand.drawCard(7, uno) # Starting amount of cards

    def displayHand(self, display_card):
        return f"Ai's hand: {self.hand.displayHand(display_card, False)}"
    
    def botTurn(self, uno, players):
        card_placed = False
        bot_cards = players[uno.turn].hand.cards

        """ Searches for valid card to place in Ai's hand """
        for item in range(len(bot_cards)):
            if ((uno.display_card.color == bot_cards[item].color or 
                 bot_cards[item].color == "wild") or 
                 uno.display_card.number == bot_cards[item].number):
                print(f"\n\033[32m===== A {bot_cards[item]} was placed! =====\033[0m")
                uno.placeCard(bot_cards, item) # Places Card from hand
                uno.checkEffect(players, uno) # Applies effects skip, plus, or reverse
                card_placed = True
                break # Ends card search after card is placed
        
        """ If no card in hand is placeable """
        if card_placed == False:
            print("\n\033[32m===== Drew a card! =====\033[0m")
            players[uno.turn].hand.drawCard(1, uno)