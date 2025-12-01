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
            print(f"\n\033[33m===== Your turn =====\033[0m")
        else:
            print(f"\n\033[33m===== Player {uno.turn + 1} turn =====\033[0m")


        if (uno.turn == 0): # During the player's turn
            
            print(f"Current card: {uno.game_card.color}_{uno.game_card.number}")
            print(f"Cards in hand: {players[0].hand}")
            decision = input("\nPress enter to continue: ")
            
            if (decision == "d"):
                print("\n\033[32m===== Drew a card! =====\033[0m")
                players[0].hand.drawCard(1)
                uno.nextTurn()

            if decision.isdigit():
                card_num = int(decision)-1
                if (int(decision) >= 1 and int(decision) <= len(players[0].hand.cards)):

                    """ If the card or number is the same as the current game card"""
                    if (uno.game_card.color == players[0].hand.cards[card_num].color or uno.game_card.number == players[0].hand.cards[card_num].number):
                        print(f"\n\033[32m===== A {players[0].hand.cards[card_num]} was placed! =====\033[0m")
                        uno.placeCard(players[0].hand.cards, card_num) # Places Card from hand
                        uno.checkEffect(players[0].hand, players) # Applies effects skip, plus, or reverse
                        uno.nextTurn() # Goes to the next turn
                    else:
                        print("\n///// Invalid Card Selected /////")
        

        elif (uno.turn != 0): # During the AI's turn

            card_placed = 0
            current_bot = players[uno.turn]
            current_card = uno.game_card
            print(f"Current card: {current_card}")
            print(current_bot)

            """ If the card or number is the same as the current game card"""
            for item in range(len(current_bot.hand.cards)):
                if (uno.game_card.color == current_bot.hand.cards[item].color or uno.game_card.number == current_bot.hand.cards[item].number):
                    print(f"\n\033[32m===== A {current_bot.hand.cards[item]} was placed! =====\033[0m")
                    uno.placeCard(current_bot.hand.cards, item) # Places Card from hand
                    uno.checkEffect(current_bot.hand, players) # Applies effects skip, plus, or reverse
                    uno.nextTurn()
                    card_placed = 1
                    break # Ends card search after card is placed
            
            if (card_placed == 0):
                print("\n\033[32m===== Drew a card! =====\033[0m")
                current_bot.hand.drawCard(1)
                uno.nextTurn()
            

                


if __name__ == "__main__":
    main()