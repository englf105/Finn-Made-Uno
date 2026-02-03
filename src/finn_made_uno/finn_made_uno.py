"""
Uno Game
by: Finn English
"""


from game import Game


def main():

    """ Game setup """
    uno = Game()
    players = []
    uno.addPlayers(players, uno)
    least_cards = len(players[uno.turn].hand.cards)

    """ Game Loop """
    while len(players[uno.turn].hand.cards) != 0:
        uno.displayTurnInfo(players)
        uno.playerTurn(players, uno)
        if least_cards > len(players[uno.turn].hand.cards):
            least_cards = len(players[uno.turn].hand.cards)
        if least_cards == 0: break
        uno.nextTurn()

    print(f"\n\033[34m===== Player {uno.turn + 1} won Uno! =====\033[0m\n")
                
                
if __name__ == "__main__":
    main()