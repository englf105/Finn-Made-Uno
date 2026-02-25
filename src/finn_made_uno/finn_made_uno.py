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

    """ Settings """
    uno.place_after_draw = False
    uno.draw_till_place = False
    uno.stack_plus_cards = False

    """ Game Loop """
    while any(player.hand.cards for player in players):
        uno.displayTurnInfo(players)
        uno.playerTurn(players, uno)
        uno.nextTurn()

    print(f"\n\033[34m===== Player {uno.turn + 1} won Uno! =====\033[0m\n")
                
                
if __name__ == "__main__":
    main()