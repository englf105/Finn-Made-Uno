import hand


class Player:

    def __init__(self, uno):
        self.hand = hand.Hand() # Creating the player's hand
        self.hand.drawCard(7, uno) # Starting amount of cards

    def displayHand(self, display_card):
        return f"Cards in hand: {self.hand.displayHand(display_card, True)}"
    
    def playerTurn(self, uno, players):
        print(
                "\n=== Options ===" +
                "\n-Draw (d)" + 
            f"\n-Play a card (1-{len(self.hand.cards)})"
        )

    def playCard(self, uno, card):
        player_cards = self.hand.cards
        
        if (uno.validCard(card)):
                """ If the card or number is the same as the current game card """
                print(f"\n\033[32m===== A {card} was placed! =====\033[0m")
                uno.placeCard(player_cards, card) # Places Card from hand
                uno.checkEffect() # Applies effects skip, plus, or reverse
                uno.nextTurn() # Goes to the next turn
                return True
                 
        else: print("\n///// Cannot play card. /////")

    def drawCard(self, uno):
        print(f"\n\033[32m===== {uno.displayName(uno.turn, False)} drew a card! =====\033[0m")
        uno.players[0].hand.drawCard(1, uno)

        """ Game Rules """
        if uno.place_after_draw:
            can_place = False
            for item in self.hand.cards:
                if uno.validCard(item):
                    can_place = True
                    print("\n===== Drawn card can be placed! =====")
                    return True

            if not can_place:
                print("\n===== Drawn card cannot be placed! =====")
                uno.nextTurn() # Goes to the next turn
                return True

        elif uno.draw_till_place:
            return True
                
        if not uno.draw_till_place and not uno.place_after_draw: 
            print("\n===== No other rules selected. =====")
            uno.nextTurn() # Goes to the next turn
            return True
        


