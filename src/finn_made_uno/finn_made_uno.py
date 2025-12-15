"""
Uno Game
by: Finn English
"""


import game
from player import Player
from player_ai import Ai


def main():

    uno = game.Game()

    players = []
    players.append(Player())
    for item in range(uno.player_amount):
        players.append(Ai())

    least_cards = len(players[uno.turn].hand.cards)

    # Game Loop
    while (len(players[uno.turn].hand.cards) != 0):

        uno.displayTurnInfo(players)

        if isinstance(players[uno.turn], Player): # During the player's turn
            Player.playerTurn(uno, players)

        elif isinstance(players[uno.turn], Ai): # During the AI's turn
            Ai.botTurn(uno, players)

        if least_cards > len(players[uno.turn].hand.cards):
            least_cards = len(players[uno.turn].hand.cards)
        if least_cards == 0:
            break

        uno.nextTurn() # Goes to the next turn

    print(f"\n\033[34m===== Player {uno.turn + 1} won Uno! =====\033[0m\n")
        
                
if __name__ == "__main__":
    main()