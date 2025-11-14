import hand

class Ai:
    
    def __init__(self):
        self.hand = hand.Hand() # Creating the player's hand
        self.hand.drawCard(7) # Starting amount of cards

    def __str__(self):
        print(f"\nAi's Hand: {self.hand}")