import hand

class Player:

    def __init__(self):
        self.hand = hand.Hand() # Creating the player's hand
        self.hand.drawCard(7) # Starting amount of cards