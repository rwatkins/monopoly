import random

class Board:
    available_hotels = 12
    available_houses = 32
    free_parking = 0
    
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
                advance_to_go()
            ),
            Chance(
                "Advance to Illinois Ave.",
                advance_to_illinois_ave()
            ),
            Chance(
                """Advance token to nearest Utility. If unowned, you may buy it
                from the Bank. If owned, throw dice and pay owner a total of
                ten times the amount thrown.""",
                advance_to_nearest_utility()
            ),
            Chance(
                "Bank pays you dividend of $50",
            ),
            Chance(
                "Go back 3 spaces",
                go_back()
            ),
            Chance(
                "Go directly to Jail -- do not pass Go, do not collect $200",
                go_directly_to_jail()
            ),
            Chance(
                """Make general repairs on all your property - for each house
                pay $25 - for each hotel $100""",
                make_general_repairs()
            ),
            Chance(
                "Pay poor tax of $15",
                pay_poor_tax()
            ),
            Chance(
                """Take a trip to Reading Railroad -- if you pass Go collect
                $200""",
                advance_to_reading_railroad()
            ),
            Chance(
                """Take a walk on the Boardwalk -- advance token to board
                walk""",
                advance_to_boardwalk()
            ),
            Chance(
                """You have been elected chairman of the board -- pay each
                player $50""",
                pay_each_player()
            ),
            Chance(
                "Your building loan matures -- collect $150",
                building_loan()
            ),
            Chance(
                "You have won a crossword competition -- collect $100",
                crossword_competition()
            )
        ]
        
        # Community Chest cards
        self.community_chest = []

class Chance:
    def __init__(self, text, function):
        self.text = text
        self.function = function

class Property:
    hotel = False
    houses = 0
    
    def __init__(self, name, group, price=0, mandatory=False):
        self.name = name
        self.group = group
        self.price = price
        self.mandatory = mandatory
        self.is_purchasable = not (self.group == "Special" or self.group == "Tax")
        self.owner = Player # this will be a Player object

class Player:
    def __init__(self, name, money=1500):
        self.name = name
        self.money = money
        self.pos = pos # starting position on the board, from 0 to 39
        self.status = "OK" # OK, In Jail, Loser, Winner
        self.doubles_counter = 0
        self.has_get_out_of_jail_free_card = False
    
    def move_to(self, pos, pass_go=True):
        self.pos = pos
        if self.pos > pos and pass_go: self.money += 200
    
    def set_status(self, status):
        self.status = status

def roll_dice(self, num_of_dice):
    sides = 6
    result = []
    for n in range(1, num_of_dice + 1):
        result.append(random.randrange(1, sides + 1))
    return result

# Chance functions
def advance_to_go(board, player, players):
    player.move_to(0)
    return

def advance_to_illinois_ave(board, player, players):
    player.move_to(24)
    return

def advance_to_nearest_utility(board, player, players):
    player.move_to(get_nearest("Utility", player.pos, board.properties))
    if len(board.properties[player.pos].owner.name):
        dice = random.randrange(2, 13)
        player.money -= 10 * dice
        board.properties[player.pos].owner.money += 10 * dice
    else:
        # prompt for purchase
        pass
    return

def advance_to_nearest_railroad(board, player, players):
    player.move_to(get_nearest("Railroad", player.pos, board.properties))
    if len(board.properties[player.pos].owner.name):
        # pay owner twice the rent he/she is owed
        pass
    else:
        # prompt for purchase
        pass
    return

def advance_to_st_charles_place(board, player, players):
    player.move_to(11)
    return

def bank_pays_dividend(board, player, players):
    player.money += 50
    return

def get_out_of_jail_free_card(board, player, players):
    player.hasGetOutOfJailFreeCard = True
    return

def go_back(board, player, players):
    player.move_to(player.pos - 3, False)
    return

def go_directly_to_jail(board, player, players):
    player.move_to(10, False)
    player.set_status("In Jail")
    return

def make_general_repairs(board, player, players):
    cost = 0
    for x in player.properties:
        if x.hotel:
            cost += 100
        elif x.houses:
            cost += x.houses * 25
    player.money -= cost
    board.freeParking += cost
    return

def pay_poor_tax(board, player, players):
    player.money -= 15
    board.freeParking += 15
    return

def advance_to_reading_railroad(board, player, players):
    player.move_to(5)
    return

def advance_to_boardwalk(board, player, players):
    player.move_to(39)
    return

def pay_each_player(board, player, players):
    for p in players:
        if p.status != "Loser":
            player -= 50
            p += 50
    return

def building_loan(board, player, players):
    player.money += 150
    return

def crossword_competition(board, player, players):
    player.money += 100
    return

def get_nearest(group, pos, properties):
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
