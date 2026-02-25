import hand


class Player:

    def __init__(self, uno):
        self.hand = hand.Hand() # Creating the player's hand
        self.hand.drawCard(7, uno) # Starting amount of cards

    def displayHand(self, display_card):
        return f"Cards in hand: {self.hand.displayHand(display_card, True)}"
    
    def playerTurn(self, uno, players):
        while True:
            decision = input(
                "\n=== Options ===" +
                "\n-Draw (d)" + 
                f"\n-Play a card (1-{len(self.hand.cards)})" +
                "\n\nEnter decision here: "
                )
            if decision.isdigit():
                card_num = int(decision)-1
                player_cards = players[0].hand.cards
                if int(decision) >= 1 and int(decision) <= len(player_cards):

                    """ If the card or number is the same as the current game card """
                    if (uno.validCard(player_cards[card_num])):
                        print(f"\n\033[32m===== A {player_cards[card_num]} was placed! =====\033[0m")
                        uno.placeCard(player_cards, player_cards[card_num]) # Places Card from hand
                        uno.checkEffect(players, uno) # Applies effects skip, plus, or reverse
                        break
                    else:
                        print("\n///// Cannot play card. /////")
                else:
                    print("\n///// Card selected nonexistant. /////")

            elif decision == "D" or decision == "d":
                print(f"\n\033[32m===== {uno.displayName(uno.turn, False)} drew a card! =====\033[0m")
                players[0].hand.drawCard(1, uno)

                """ Game Rules """
                if uno.place_after_draw:
                    can_place = False
                    for item in self.hand.cards:
                        if uno.validCard(item):
                            can_place = True
                            print("\n===== Drawn card can be placed! =====")
                            break
                    if not can_place:
                        break

                if not uno.draw_till_place and not uno.place_after_draw: 
                    break

                uno.displayTurnInfo(players)

            else:
                print("\n///// Select a card by entering it's number or" +
                " enter d to draw a card. /////")
