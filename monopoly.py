import random

class Board:
    availableHotels = 12
    availableHouses = 32
    freeParking = 0
    
    def __init__(self):
        # Properties around the board (every possible space to land on)
        self.properties = (
            Property("GO", "Special"), # 0
            Property("Mediterranean Avenue", "Purple", 60),
            Property("Community Chest", "Special"),
            Property("Baltic Avenue", "Purple", 60),
            Property("Income Tax", "Special"),
            Property("Reading Railroad", "Railroad", 200),
            Property("Oriental Avenue", "Light Blue", 100),
            Property("Chance", "Special"),
            Property("Vermont Avenue", "Light Blue", 100),
            Property("Connecticut Avenue", "Light Blue", 120),
            Property("Jail", "Special"), # 10
            Property("St. Charles Place", "Magenta", 140),
            Property("Electric Company", "Utility", 150),
            Property("States Avenue", "Magenta", 140),
            Property("Virginia Avenue", "Magenta", 160),
            Property("Pennsylvania Railroad", "Railroad", 200),
            Property("St. James Place", "Orange", 180),
            Property("Community Chest", "Special"),
            Property("Tennessee Avenue", "Orange", 180),
            Property("New York Avenue", "Orange", 200),
            Property("Free Parking", "Special"), # 20
            Property("Kentucky Avenue", "Red", 220),
            Property("Chance", "Special"),
            Property("Indiana Avenue", "Red", 220),
            Property("Illinois Avenue", "Red", 240),
            Property("B&O Railroad", "Railroad", 200),
            Property("Atlantic Avenue", "Yellow", 260),
            Property("Ventnor Avenue", "Yellow", 260),
            Property("Water Works", "Utility", 150),
            Property("Marvin Gardens", "Yellow", 280),
            Property("GO TO JAIL", "Special"), # 30
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
                "Advance to Go (Collect $200)",
                advanceToGo()
            ),
            Chance(
                "Advance to Illinois Ave.",
                advanceToIllinoisAve()
            ),
            Chance(
                """Advance token to nearest Utility. If unowned, you may buy it
                from the Bank. If owned, throw dice and pay owner a total of
                ten times the amount thrown.""",
            ),
            Chance(
                "Bank pays you dividend of $50",
            ),
            Chance(
                """Make general repairs on all your property - for each house
                pay $25 - for each hotel $100""",
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
    hotel = False
    houses = 0
    
    def __init__(self, name, group, price=0, mandatory=False):
        self.name = name
        self.group = group
        self.price = price
        self.mandatory = mandatory
        self.isPurchasable = not (self.group == "Special" or self.group == "Tax")
        self.owner = Player # this will be a Player object

class Player:
    pos = 0 # starting position on the board, from 0 to 39
    status = "OK" # OK, In Jail, Loser, Winner
    doublesCounter = 0
    hasGetOutOfJailFreeCard = False
    
    def __init__(self, name, money=1500):
        self.name = name
        self.money = money
    
    def moveTo(self, pos, passGo=True):
        self.pos = pos
        if self.pos > pos and passGo: self.money += 200
    
    def setStatus(self, status):
        self.status = status

def rollDice(self, num):
    sides = 6
    result = []
    for n in range(1, num + 1):
        result.append(random.randrange(1, sides + 1))
    return result

# Chance functions
def advanceToGo(board, player, players):
    player.moveTo(0)
    return

def advanceToIllinoisAve(board, player, players):
    player.moveTo(24)
    return

def advanceToNearestUtility(board, player, players):
    player.moveTo(getNearest("Utility", player.pos, board.properties))
    if len(board.properties[player.pos].owner.name):
        dice = random.randrange(2, 13)
        player.money -= 10 * dice
        board.properties[player.pos].owner.money += 10 * dice
    else:
        # prompt for purchase
        pass
    return

def advanceToNearestRailroad(board, player, players):
    player.moveTo(getNearest("Railroad", player.pos, board.properties))
    if len(board.properties[player.pos].owner.name):
        # pay owner twice the rent he/she is owed
        pass
    else:
        # prompt for purchase
        pass
    return

def advanceToStCharlesPlace(board, player, players):
    player.moveTo(11)
    return

def bankPaysDividend(board, player, players):
    player.money += 50
    return

def getOutOfJailFreeCard(board, player, players):
    player.hasGetOutOfJailFreeCard = True
    return

def goBack(board, player, players):
    player.moveTo(player.pos - 3, False)
    return

def goDirectlyToJail(board, player, players):
    player.moveTo(10, False)
    player.setStatus("In Jail")
    return

def makeGeneralRepairs(board, player, players):
    cost = 0
    for x in player.properties:
        if x.hotel:
            cost += 100
        elif x.houses:
            cost += x.houses * 25
    player.money -= cost
    board.freeParking += cost
    return

def payPoorTax(board, player, players):
    player.money -= 15
    board.freeParking += 15
    return

def advanceToReadingRailroad(board, player, players):
    player.moveTo(5)
    return

def advanceToBoardwalk(board, player, players):
    player.moveTo(39)
    return

def payEachPlayer(board, player, players):
    for p in players:
        if p.status != "Loser":
            player -= 50
            p += 50
    return

def buildingLoan(board, player, players):
    player.money += 150
    return

def crosswordCompetition(board, player, players):
    player.money += 100
    return

def getNearest(group, pos, properties):
    '''Returns index of nearest Utility to the given position'''
    # first look through all the properties from current position to the end
    # of the board
    for x in properties[pos:]:
        if x.group == group:
            return properties.index(x)
    
    # then look through all the properties from the beginning of the board up
    # to the current position
    for x in properties[:pos]:
        if x.group == group:
            return properties.index(x)

if __name__ == '__main__':
    print "Welcome to Monopoly!"
