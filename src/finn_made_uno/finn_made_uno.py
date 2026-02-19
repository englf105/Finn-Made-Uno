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
    uno.place_after_draw = True
    uno.draw_till_place = False
    uno.stack_plus_cards = False

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