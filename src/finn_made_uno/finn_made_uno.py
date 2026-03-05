"""
Uno Game
by: Finn English
"""


from game import Game


def main():

    """ Game Setup """
    uno = Game()

    """ Settings """
    uno.place_after_draw = False # Working
    uno.draw_till_place = False # Working
    uno.stack_plus_cards = True # In progress

    """ Game Loop """
    while uno.playerHasCards():
        uno.displayTurnInfo()
        uno.playerTurn()
        uno.nextTurn()
    
    """ Game Loop Ends """
    print(uno.winnerMessage())
                
                
if __name__ == "__main__":
    main()