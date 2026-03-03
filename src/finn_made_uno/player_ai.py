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
        if uno.stack_plus_cards:
            for item in bot_cards:
                if item.number == "plus":
                    print(f"\n\033[32m===== A {item} was placed! =====\033[0m")
                    uno.placeCard(bot_cards, item) # Places Card from hand
                    uno.checkEffect() # Applies effects skip, plus, or reverse
                    card_placed = True
                    break # Ends card search after card is placed
            
        if not card_placed:
            for item in bot_cards:
                if uno.validCard(item):
                    print(f"\n\033[32m===== A {item} was placed! =====\033[0m")
                    uno.placeCard(bot_cards, item) # Places Card from hand
                    uno.checkEffect() # Applies effects skip, plus, or reverse
                    card_placed = True
                    break # Ends card search after card is placed
        
        """ If no card in hand is placeable """
        if not card_placed:
            print(f"\n\033[32m===== {uno.displayName(uno.turn, False)} drew a card! =====\033[0m")
            players[uno.turn].hand.drawCard(1, uno)
            if uno.draw_till_place:
                self.botTurn(uno, players)
            elif uno.place_after_draw and not uno.draw_till_place:
                can_place = False
                for item in self.hand.cards:
                    if uno.validCard(item):
                        can_place = True
                if can_place:
                    self.botTurn(uno, players)

        