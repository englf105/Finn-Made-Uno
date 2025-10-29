"""
Uno Game
by: Finn English
"""

import card

class Game():
    
    turn = 1
    player_quantity = 4
    
    game_card = card.Card.randomCard()

    while (game_card[0] == "skip"):
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
        
        print(f"Current card number: {Game.game_card[0]}")
        print(f"Current card color: {Game.game_card[1]}")
        ready = input("\nPress enter to continue: ")
        
        if (ready == "r"):
            order_multiplier = order_multiplier * -1
            print("\n===== The turns are reversed! =====")
        
        if (ready == "s"):
            Game.turn += (1 * order_multiplier)
            if (Game.turn > Game.player_quantity):
                Game.turn = 1
            if (Game.turn) < 1:
                Game.turn = Game.player_quantity
            print("\n===== A turn was skipped! =====")
            
        Game.nextTurn(Game, order_multiplier)


if __name__ == "__main__":
    main()