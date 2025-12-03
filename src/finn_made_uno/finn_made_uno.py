"""
Uno Game
by: Finn English
"""


import game
import player
import player_ai


def main():

    uno = game.Game()

    players = []
    players.append(player.Player())
    for i in range(uno.player_amount):
        players.append(player_ai.Ai())

    least_cards = len(players[uno.turn].hand.cards)

    # Game Loop
    while (least_cards > 0):

        uno.displayTurnInfo(players)

        if (uno.turn == 0): # During the player's turn
            
            decision = input("\nPress enter to continue: ")
            
            if (decision == "d"):
                print("\n\033[32m===== Drew a card! =====\033[0m")
                players[0].hand.drawCard(1)
                uno.nextTurn()

            if decision.isdigit():
                card_num = int(decision)-1
                player_cards = players[0].hand.cards
                if (int(decision) >= 1 and int(decision) <= len(players[0].hand.cards)):

                    """ If the card or number is the same as the current game card"""
                    if (uno.game_card.color == player_cards[card_num].color or uno.game_card.number == player_cards[card_num].number):
                        print(f"\n\033[32m===== A {player_cards[card_num]} was placed! =====\033[0m")
                        uno.placeCard(player_cards, card_num) # Places Card from hand
                        uno.checkEffect(players) # Applies effects skip, plus, or reverse
                        uno.checkWin(players, least_cards)
                        uno.nextTurn() # Goes to the next turn
                    else:
                        print("\n///// Invalid Card Selected /////")
        
        elif (uno.turn != 0): # During the AI's turn

            card_placed = 0
            current_bot = players[uno.turn]
            bot_cards = players[uno.turn].hand.cards

            """ If the card or number is the same as the current game card"""
            for item in range(len(bot_cards)):
                if (uno.game_card.color == bot_cards[item].color or uno.game_card.number == bot_cards[item].number):
                    print(f"\n\033[32m===== A {bot_cards[item]} was placed! =====\033[0m")
                    uno.placeCard(bot_cards, item) # Places Card from hand
                    uno.checkEffect(players) # Applies effects skip, plus, or reverse
                    uno.checkWin(players, least_cards)
                    uno.nextTurn()
                    card_placed = 1
                    break # Ends card search after card is placed
            
            if (card_placed == 0):
                print("\n\033[32m===== Drew a card! =====\033[0m")
                current_bot.hand.drawCard(1)
                uno.nextTurn()

    print(f"\n\033[34m===== Player {uno.turn + 1} won Uno! =====\033[0m\n")
        
                
if __name__ == "__main__":
    main()