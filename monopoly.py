import copy
import random

DEFAULT_CHANCE_DECK = [
    Chance(
        "Advance to Go (Collect $200)",
        advance_to_go
    ),
    Chance(
        "Advance to Illinois Ave.",
        advance_to_illinois_ave
    ),
    Chance(
        """Advance token to nearest Utility. If unowned, you may buy it
        from the Bank. If owned, throw dice and pay owner a total of
        ten times the amount thrown.""",
        advance_to_nearest_utility
    ),
    Chance(
        "Bank pays you dividend of $50",
        bank_pays_dividend
    ),
    Chance(
        "Go back 3 spaces",
        go_back
    ),
    Chance(
        "Go directly to Jail -- do not pass Go, do not collect $200",
        go_directly_to_jail
    ),
    Chance(
        """Make general repairs on all your property - for each house
        pay $25 - for each hotel $100""",
        make_general_repairs
    ),
    Chance(
        "Pay poor tax of $15",
        pay_poor_tax
    ),
    Chance(
        """Take a trip to Reading Railroad -- if you pass Go collect
        $200""",
        advance_to_reading_railroad
    ),
    Chance(
        """Take a walk on the Boardwalk -- advance token to board
        walk""",
        advance_to_boardwalk
    ),
    Chance(
        """You have been elected chairman of the board -- pay each
        player $50""",
        pay_each_player
    ),
    Chance(
        "Your building loan matures -- collect $150",
        building_loan
    ),
    Chance(
        "You have won a crossword competition -- collect $100",
        crossword_competition
    )
]

class Board:
    """
    The game board containing the Chance and Community Chest cards, and the 40
    squares around the edge.
    """
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
        self.chance = copy.deepcopy(DEFAULT_CHANCE_DECK)

        # Community Chest cards
        self.community_chest = []

class Chance:
    """A card from the Chance deck."""
    def __init__(self, description, func):
        self.description = description
        self.func = func

class Property:
    """A single square on the game board."""
    def __init__(self, name, group, price=0, mandatory=False):
        self.name = name
        self.group = group
        self.price = price
        self.mandatory = mandatory
        self.is_purchasable = self.group != "Special" and self.group != "Tax"
        self.owner = None # this will be a Player object
        self.hotel = False
        self.houses = 0

class Player:
    def __init__(self, name, money=1500):
        self.name = name
        self.money = money
        self.pos = 0 # starting position on the board, from 0 to 39
        self.doubles_counter = 0
        self.has_get_out_of_jail_free_card = False

    def move_to(self, pos, pass_go=True):
        """
        Moves the Player to a specified square. If the Player passes Go, his
        money is increased by 200.
        """
        if self.pos > pos and pass_go:
            self.money += 200
        self.pos = pos

    def status(self):
        print self.name
        print self.money
        print self.pos

def roll_dice(num_of_dice=1):
    """
    Returns a list of length num_of_dice, with each element containing the
    number that was rolled on that die.
    """
    sides = 6
    result = []
    for n in range(1, num_of_dice+1):
        result.append(random.randrange(1, sides+1))
    return result

#
# Chance functions
#
def advance_to_go(**kwargs):
    """Advance to Go (Collect $200)"""
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player = kwargs["player"]
    player.move_to(0)
    return

def advance_to_illinois_ave(**kwargs):
    """Advance to Illinois Ave."""
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player = kwargs["player"]
    player.move_to(24)
    return

def advance_to_nearest_utility(**kwargs):
    """
    Advance token to nearest Utility. If unowned, you may buy it from the
    Bank. If owned, throw dice and pay owner a total of ten times the amount
    thrown.
    """
    assert "board" in kwargs.keys(), "'board' not found in arguments"
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    board = kwargs["board"]
    player = kwargs["player"]
    player.move_to(get_nearest("Utility", player.pos, board.properties))
    owner = board.properties[player.pos].owner
    if owner:
        print "Owner of", board.properties[player.pos].name, "is", owner.name
        dice = random.randrange(2, 13)
        print player.name, "rolled", dice
        print player.name, "pays", owner.name, "$", 10 * dice
        player.money -= 10 * dice
        owner.money += 10 * dice
    else:
        # prompt for purchase
        pass
    return

def bank_pays_dividend(**kwargs):
    """Bank pays you dividend of $50"""
    assert "player" in kwargs.keys(), "'player' on found in arguments"
    player = kwargs["player"]
    player.money += 50
    return

def go_back(**kwargs):
    """Go back 3 spaces"""
    assert "player" in kwargs.keys(), "'player' on found in arguments"
    player = kwargs["player"]
    player.move_to(player.pos - 3, False)
    return

def go_directly_to_jail(**kwargs):
    """Go directly to Jail -- do not pass Go, do not collect $200"""
    assert "player" in kwargs.keys(), "'player' on found in arguments"
    player = kwargs["player"]
    player.move_to(10, False)
    player.set_status("In Jail")
    return

def make_general_repairs(**kwargs):
    """
    Make general repairs on all your property - for each house pay $25 -
    for each hotel $100
    """
    assert "board" in kwargs.keys(), "'board' not found in arguments"
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    board = kwargs["board"]
    player = kwargs["player"]
    cost = 0
    for x in player.properties:
        if x.hotel:
            cost += 100
        elif x.houses:
            cost += x.houses * 25
    player.money -= cost
    board.freeParking += cost
    return

def pay_poor_tax(**kwargs):
    """Pay poor tax of $15"""
    assert "board" in kwargs.keys(), "'board' not found in arguments"
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player, board = kwargs["player"], kwargs["board"]
    player.money -= 15
    board.freeParking += 15
    return

def advance_to_reading_railroad(**kwargs):
    """Take a trip to Reading Railroad -- if you pass Go collect $200"""
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player = kwargs["player"]
    player.move_to(5)
    return

def advance_to_boardwalk(**kwargs):
    """Take a walk on the Boardwalk -- advance token to board walk"""
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player = kwargs["player"]
    player.move_to(39)
    return

def pay_each_player(**kwargs):
    """You have been elected chairman of the board -- pay each player $50"""
    assert "players" in kwargs.keys(), "'players' not found in arguments"
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    players, player = kwargs["players"], kwargs["player"]
    for p in players:
        if p.status != "Loser":
            player -= 50
            p += 50
    return

def building_loan(**kwargs):
    """Your building loan matures -- collect $150"""
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player = kwargs["player"]
    player.money += 150
    return

def crossword_competition(**kwargs):
    """You have won a crossword competition -- collect $100"""
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player = kwargs["player"]
    player.money += 100
    return

#def advance_to_nearest_railroad(**kwargs):
#    player.move_to(get_nearest("Railroad", player.pos, board.properties))
#    if len(board.properties[player.pos].owner.name):
#        # pay owner twice the rent he/she is owed
#        pass
#    else:
#        # prompt for purchase
#        pass
#    return
#
#def advance_to_st_charles_place(**kwargs):
#    player.move_to(11)
#    return
#
#def get_out_of_jail_free_card(**kwargs):
#    player.has_get_out_of_jail_free_card = True
#    return

def get_nearest(group, pos, properties):
    """Returns index of nearest Utility to the given position"""
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

def special_property(property_name, board, player, players):
    action = {
        "Chance": board.chance.pop(),
        "Pass": lambda: pass,
    }.get(property_name, "Pass")
    return action(board=board, player=player, players=players)

def run():
    board = Board()
    players = []
    players.append(Player("Riley"))
    current_round = 0

    print "Welcome to Monopoly!"
    print "Starting new game..."

    while True:
        current_round += 1
        print "Round ", current_round

        for player in players:
            print "%s's turn" % player.name

            # Player roll's dice
            dice = roll_dice(2)
            print "rolled " % player.name, dice

            # Move number of spaces on dice
            player.move_to(player.pos+sum(dice))
            current_square = board.properties[player.pos].name
            current_group = board.properties[player.pos].group
            print "%s landed on %s" % player.name, current_square

            action = {
                "Special": special_property(property_name=current_square,
                                            board=board, player=player,
                                            players=players),
                "Pass": lambda: pass,
            }.get(current_group, "Pass")

            action()

            # End of turn
            raw_input("Press Enter to end this player's turn")
            print "End of %s's turn" % player.name

if __name__ == '__main__':
    run()
