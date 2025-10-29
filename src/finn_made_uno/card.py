import random


class Card:

    # List of numbers and colors
    number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "skip", "reverse", "plus"]
    color = ["red", "yellow", "blue", "green"]
    
    def __init__(self, number, color):
        self.number =  number
        self.color = color

    # Getting a random card from the deck
    def randomCard():
        random_num = random.choice(Card.number)
        random_color = random.choice(Card.color)
        return [random_num, random_color]