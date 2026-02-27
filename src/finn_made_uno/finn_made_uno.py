"""
Uno Game
by: Finn English
"""


from game import Game


def main():

    """ Game Setup """
    uno = Game()
    players = []
    uno.addPlayers(players, uno)

    """ Settings """
    uno.place_after_draw = False
    uno.draw_till_place = False
    uno.stack_plus_cards = True

    """ Game Loop """
    while uno.checkPlayerCards(players):
        uno.displayTurnInfo(players)
        uno.playerTurn(players, uno)
        uno.nextTurn()
    
    """ Game Loop Ends """
    print(uno.winnerName(players))
                
                
if __name__ == "__main__":
    main()