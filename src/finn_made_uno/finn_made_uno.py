"""
Uno Game
by: Finn English
"""


import game
import player
import player_ai


def main():

    uno = game.Game()
    card_quantity = 7

    uno.setRandomCard()
    uno.checkPlayerAmount()

    players = []

    players.append(player.Player())

    for i in range(uno.player_amount):
        players.append(player_ai.Ai())

    # Game Loop
    while (card_quantity > 0):
        
        """ Diplaying whose turn it is in the console"""
        if (uno.turn == 0):
            print(f"\n===== Your turn =====")
        else:
            print(f"\n===== Player {uno.turn + 1} turn =====")


        if (uno.turn == 0): # During the player's turn
            
            print(f"Current card: {uno.game_card.color}_{uno.game_card.number}")
            print(f"Cards in hand: {players[0].hand}")
            decision = input("\nPress enter to continue: ")
            
            if (decision == "d"):
                players[0].hand.drawCard(1)
                print("\n===== Drew a card! =====")

            if decision.isdigit():
                card_num = int(decision)-1
                if (int(decision) >= 1 and int(decision) <= len(players[0].hand.cards)):

                    """ If the card or number is the same as the current game card"""
                    if (uno.game_card.color == players[0].hand.cards[card_num].color or uno.game_card.number == players[0].hand.cards[card_num].number):

                        print(f"\n===== A {players[0].hand.cards[card_num]} was placed! =====")
                        uno.placeCard(players[0].hand.cards, card_num) # Places Card from hand
                        uno.checkEffect(players[0].hand, players) # Applies effects skip, plus, or reverse
                        uno.nextTurn() # Goes to the next turn

                    else:
                        print("\n///// Invalid Card Selected /////")
        

        elif (uno.turn != 0): # During the AI's turn
            current_bot = players[uno.turn]
            print(current_bot)
            uno.nextTurn()
#            for j in range(len(current_bot.hand.cards)):
#                if (uno.game_card[0] == (current_bot.hand.cards[card_num][0])):
                


if __name__ == "__main__":
    main()