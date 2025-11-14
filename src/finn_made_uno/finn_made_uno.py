"""
Uno Game
by: Finn English
"""


import game
import player
import player_ai


def main():

    uno = game.Game()
    my_player = player.Player()
    card_quantity = 7
    order_multiplier = 1

    uno.setRandomCard()
    uno.checkPlayerAmount()

    players = []
    for i in range(uno.player_amount - 1):
        players.append(player_ai.Ai())

    # Game Loop
    while (card_quantity > 0):
        
        """ Diplaying whose turn it is in the console"""
        if (uno.turn == 1):
            print(f"\n===== Your turn =====")
        else:
            print(f"\n===== Player {uno.turn} turn =====")


        if (uno.turn == 1): # During the player's turn
            
            print(f"Current card color: {uno.game_card[0]}")
            print(f"Current card number: {uno.game_card[1]}")
            print(f"Cards in hand: {my_player.hand}")
            decision = input("\nPress enter to continue: ")
            
            if (decision == "d"):
                my_player.hand.drawCard(1)
                print("\n===== Drew a card! =====")

            if decision.isdigit():
                card_num = int(decision)-1
                if (int(decision) >= 1 and int(decision) <= len(my_player.hand.cards)):

                    """ If the card or number is the same as the current game card"""
                    if (uno.game_card[0] == my_player.hand.cards[card_num][0] or uno.game_card[1] == my_player.hand.cards[card_num][1]):

                        print(f"\n===== A {my_player.hand.cards[card_num]} was placed! =====")
                        uno.placeCard(my_player.hand.cards, card_num) # Places Card from hand
                        uno.checkEffect(my_player.hand) # Applies effects skip, plus, or reverse
                        uno.nextTurn(order_multiplier) # Goes to the next turn

                    else:
                        print("\n///// Invalid Card Selected /////")
        

        elif (uno.turn != 1): # During the AI's turn
            uno.nextTurn(order_multiplier)
            current_bot = players[uno.turn - 2]
            print(current_bot.hand.cards)
#            for j in range(len(current_bot.hand.cards)):
#                if (uno.game_card[0] == (current_bot.hand.cards[card_num][0])):
                


if __name__ == "__main__":
    main()