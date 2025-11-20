import random


class Card:

    # List of numbers and colors
    color = ["red", "yellow", "blue", "green"]
    number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "skip", "reverse", "plus"]
    
    def __init__(self, color, number):
        self.color = color
        self.number =  number

    def __str__(self):
        rep = self.color + "_" + self.number
        return rep

    # Getting a random card from the deck
    def randomCard():
        random_color = random.choice(Card.color)
        random_num = random.choice(Card.number)
        return Card(random_color, random_num)
