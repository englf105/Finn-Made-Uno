"""
Uno Game
by: Finn English
"""


import game
from player import Player
from player_ai import Ai
from deck import Deck


def main():

    # Game setup
    deck = Deck()
    uno = game.Game(deck)
    players = []
    players.append(Player(deck, uno)) # Adds player to first player slot
    for player in range(uno.player_amount):
        players.append(Ai(deck, uno))
    least_cards = len(players[uno.turn].hand.cards)

    # Game Loop
    while (len(players[uno.turn].hand.cards) != 0):

        uno.displayTurnInfo(players)

        if isinstance(players[uno.turn], Player): # During player's turn
            Player.playerTurn(uno, players, deck)

        elif isinstance(players[uno.turn], Ai): # During AI's turn
            Ai.botTurn(uno, players, deck)

        if least_cards > len(players[uno.turn].hand.cards):
            least_cards = len(players[uno.turn].hand.cards)
        if least_cards == 0:
            break

        uno.nextTurn() # Goes to next turn

    print(f"\n\033[34m===== Player {uno.turn + 1} won Uno! =====\033[0m\n")
                
                
if __name__ == "__main__":
    main()