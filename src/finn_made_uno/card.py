
class Card:

    # List of numbers and colors
    color = ["red", "yellow", "green", "blue", "wild"]
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "plus", "skip", "reverse"]
    wild_types = ["card", "plus_4"]
    
    def __init__(self, color, number):
        self.color = color
        self.number =  number

    def __str__(self):
        rep = self.color + "_" + self.number
        return rep
