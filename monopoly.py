import random

def __init__(self):
    self.players = []
    self.players.append(Player("Riley"))
    self.players.append(Player("Scott"))
    b = Board()

class Board:
    def __init__(self):
        # Properties around the board (every possible space to land)
        self.properties = (
            Property("GO", "Special"),
            Property("Mediterranean Avenue", "Purple", 60),
            Property("Community Chest", "Special"),
            Property("Baltic Avenue", "Purple", 60),
            Property("Income Tax", "Special"),
            Property("Reading Railroad", "Railroad", 200),
            Property("Oriental Avenue", "Light Blue", 100),
            Property("Chance", "Special"),
            Property("Vermont Avenue", "Light Blue", 100),
            Property("Connecticut Avenue", "Light Blue", 120),
            Property("Jail", "Special"),
            Property("St. Charles Place", "Magenta", 140),
            Property("Electric Company", "Utility", 150),
            Property("States Avenue", "Magenta", 140),
            Property("Virginia Avenue", "Magenta", 160),
            Property("Pennsylvania Railroad", "Railroad", 200),
            Property("St. James Place", "Orange", 180),
            Property("Community Chest", "Special"),
            Property("Tennessee Avenue", "Orange", 180),
            Property("New York Avenue", "Orange", 200),
            Property("Free Parking", "Special"),
            Property("Kentucky Avenue", "Red", 220),
            Property("Chance", "Special"),
            Property("Indiana Avenue", "Red", 220),
            Property("Illinois Avenue", "Red", 240),
            Property("B&O Railroad", "Railroad", 200),
            Property("Atlantic Avenue", "Yellow", 260),
            Property("Ventnor Avenue", "Yellow", 260),
            Property("Water Works", "Utility", 150),
            Property("Marvin Gardens", "Yellow", 280),
            Property("GO TO JAIL", "Special"),
            Property("Pacific Avenue", "Green", 300),
            Property("North Carolina Avenue", "Green", 300),
            Property("Community Chest", "Special"),
            Property("Pennsylvania Avenue", "Green", 320),
            Property("Short Line", "Railroad", 200),
            Property("Chance", "Special"),
            Property("Park Place", "Blue", 350),
            Property("Luxury Tax", "Special"),
            Property("Boardwalk", "Blue", 400),
        )
        
        # Chance cards
        self.chance = [
            Chance(
                "Bank pays you dividend of $50",
                "",
                lambda x: x + 50
            ),
            Chance(
                """Make general repairs on all your property - for each house
                pay $25 - for each hotel $100""",
                "",
                lambda x,y,z: x - (25*y) - (100*z)
            )
        ]
        
        # Community Chest cards
        self.communityChest = []

class Chance:
    def __init__(self, text, advanceTo, f):
        self.text = text
        self.advanceTo = advanceTo
        self.f = f

class Property:
    def __init__(self, name, group, price=0, mandatory=False):
        self.name = name
        self.group = group
        self.price = price
        self.mandatory = mandatory
        self.isPurchasable = not (self.group == "Special" or self.group == "Tax")
        self.owner = "" # name of owner, if any

class Player:
    pos = 0 # starting position on the board, from 0 to 39
    status = "OK" # OK, In Jail, Loser, Winner
    doublesCounter = 0
    
    def __init__(self, name, money=1500):
        self.name = name
        self.money = money
    
    def moveToPos(self, pos):
        self.pos = pos
    
    def setStatus(self, status):
        self.status = status

def rollDice(self, num):
    sides = 6
    result = []
    for n in range(1, num + 1):
        result.append(random.randrange(1, sides + 1))
    return result

if __name__ == '__main__':
    print "Welcome to Monopoly!"