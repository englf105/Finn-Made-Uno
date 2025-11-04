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

    while (game_card[1] == "skip"):
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
        
        print(f"\nTurn: {self.turn}")


def main():

    card_quantity = 1
    order_multiplier = 1

    # Game Loop
    while (card_quantity > 0):
        
        print(f"Current card color: {Game.game_card[0]}")
        print(f"Current card number: {Game.game_card[1]}")

        print(f"Cards in hand: {(", ").join(player.Hand.display_cards)}")

        ready = input("\nPress enter to continue: ")
        
        if (ready == "d"):
            player.Hand.DrawCard(player, 1)
            print("\n===== Drew a card! =====")

        if ready.isdigit():
            card_num = int(ready)-1
            if (int(ready) >= 1 and int(ready) <= len(player.Hand.player_cards)):

                print(f"\n===== A {player.Hand.display_cards[card_num]} was placed! =====")

                """Set the card placed to the current card"""
                Game.game_card[0] = player.Hand.player_cards[card_num][1] # Card Number
                Game.game_card[1] = player.Hand.player_cards[card_num][0] # Card Color

                del player.Hand.player_cards[card_num]
                del player.Hand.display_cards[card_num]

        if (Game.game_card[1] == "r"):
            order_multiplier = order_multiplier * -1
            print("\n===== The turns are reversed! =====")
        
        if (Game.game_card[1] == "s"):
            Game.turn += (1 * order_multiplier)
            if (Game.turn > Game.player_quantity):
                Game.turn = 1
            if (Game.turn) < 1:
                Game.turn = Game.player_quantity
            print("\n===== A turn was skipped! =====")

        Game.nextTurn(Game, order_multiplier)


if __name__ == "__main__":
    main()