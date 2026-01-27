import hand

class Player:

    def __init__(self, uno):
        self.hand = hand.Hand() # Creating the player's hand
        self.hand.drawCard(7, uno) # Starting amount of cards

    def __str__(self):
        return f"Cards in hand: {self.hand}"
    
    def playerTurn(self, uno, players):
        while True:
            decision = input("\n=== Options ===" +
                            "\n-Draw (d)" + 
                             f"\n-Play a card (1-{len(self.hand.cards)})" +
                             "\n\nEnter decision here: ")
            if decision.isdigit():
                card_num = int(decision)-1
                player_cards = players[0].hand.cards
                if int(decision) >= 1 and int(decision) <= len(player_cards):

                    """ If the card or number is the same as the current game card"""
                    if ((uno.display_card.color == player_cards[card_num].color or 
                        player_cards[card_num].color == "wild") or 
                        uno.display_card.number == player_cards[card_num].number):

                        print(f"\n\033[32m===== A {player_cards[card_num]} was placed! =====\033[0m")
                        uno.placeCard(player_cards, card_num) # Places Card from hand
                        uno.checkEffect(players, uno) # Applies effects skip, plus, or reverse
                        break
                    else:
                        print("\n///// Invalid Card Selected /////")
                else:
                    print("\n///// Invalid Card Selected /////")

            if decision == "D" or decision == "d":
                print("\n\033[32m===== Drew a card! =====\033[0m")
                players[0].hand.drawCard(1, uno)
                break
