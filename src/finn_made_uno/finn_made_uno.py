"""
Uno Game
by: Finn English
"""

import player
import card

class Game():
    
    turn = 1
    player_quantity = 4
    game_card = card.Card.randomCard()

    while (game_card[1] == "skip" or game_card[1] == "reverse" or game_card[1] == "plus"):
        game_card = card.Card.randomCard()

    def __init__(self):
        print(f"===== Welcome to Uno! =====")
        print(f"\nTurn: {Game.turn}")
    
    def nextTurn(self, order):
        self.turn += (1 * order)
        if (self.turn > self.player_quantity):
            self.turn = 1
        if (self.turn) < 1:
            self.turn = self.player_quantity


def main():

    card_quantity = 1
    order_multiplier = 1

    player.Hand.DrawCard(7)

    # Game Loop
    while (card_quantity > 0):
        
        print(f"\nTurn: {Game.turn}")
        print(f"Current card color: {Game.game_card[0]}")
        print(f"Current card number: {Game.game_card[1]}")
        print(f"Cards in hand: {(", ").join(player.Hand.display_cards)}")

        decision = input("\nPress enter to continue: ")
        
        if (decision == "d"):
            player.Hand.DrawCard(1)
            print("\n===== Drew a card! =====")

        if decision.isdigit():
            card_num = int(decision)-1
            if (int(decision) >= 1 and int(decision) <= len(player.Hand.player_cards)):

                """ If the card or number is the same as the current game card"""
                if (Game.game_card[0] == player.Hand.player_cards[card_num][0] or Game.game_card[1] == player.Hand.player_cards[card_num][1]):

                    print(f"\n===== A {player.Hand.display_cards[card_num]} was placed! =====")

                    """ Set the card placed to the current card """
                    Game.game_card[1] = player.Hand.player_cards[card_num][1] # Card Number
                    Game.game_card[0] = player.Hand.player_cards[card_num][0] # Card Color

                    if (Game.game_card[1] == "plus"):
                        player.Hand.DrawCard(2)
                        print("\n===== Drew two more cards! =====")
                    
                    if (Game.game_card[1] == "reverse"):
                        order_multiplier = order_multiplier * -1
                        print("\n===== The turns are reversed! =====")

                    if (Game.game_card[1] == "skip"):
                        Game.turn += (1 * order_multiplier)
                        if (Game.turn > Game.player_quantity):
                            Game.turn = 1
                        if (Game.turn) < 1:
                            Game.turn = Game.player_quantity
                        print("\n===== A turn was skipped! =====")

                    """ Delete the placed card from the hand """
                    del player.Hand.player_cards[card_num] # Removing from the actual hand
                    del player.Hand.display_cards[card_num] # Removing from the terminal display

                    Game.nextTurn(Game, order_multiplier)

                else:
                    print("\n///// Invalid Card Selected /////")


if __name__ == "__main__":
    main()