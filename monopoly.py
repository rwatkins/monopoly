import copy
import random
from chance import *

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

    def __repr__(self):
        return "<%s(name='%s', group='%s', price=%s)>" % \
            (self.__class__.__name__, self.name, self.group, self.price)

class Board:
    """
    The game board containing the Chance and Community Chest cards, and the 40
    squares around the edge.
    """
    available_hotels = 12
    available_houses = 32

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

        self.free_parking = 0

    def reset_chance(self):
        self.chance = copy.deepcopy(DEFAULT_CHANCE_DECK)

class Player:
    def __init__(self, name, money=1500, pos=0):
        self.name = name
        self.money = money
        self.pos = pos # starting position on the board, from 0 to 39
        self.properties = []
        self.doubles_counter = 0
        self.has_get_out_of_jail_free_card = False
        self.status = ""

    def __repr__(self):
        return "<%s(name='%s', money=%s, pos=%s)>" % \
            (self.__class__.__name__, self.name, self.money, self.pos)

    def move_to(self, new_pos, pass_go=True):
        """
        Moves the Player to a specified square. If the Player passes Go, his
        money is increased by 200.
        """
        new_pos = new_pos % 40
        if self.pos > new_pos and pass_go:
            self.money += 200
        self.pos = new_pos

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

def run():
    board = Board()
    players = []
    players.append(Player("Riley"))
    players.append(Player("Scott"))
    current_round = 0

    print "Welcome to Monopoly!"
    print "Starting new game..."

    while True:
        current_round += 1
        print "\n\nRound", current_round, "\n"

        for player in players:
            print "%s's turn" % player.name

            # Player roll's dice
            dice = roll_dice(2)
            print "%s rolled %s" % (player.name, dice)

            # Move number of spaces on dice
            player.move_to(player.pos+sum(dice))
            property_name = board.properties[player.pos].name
            propery_group = board.properties[player.pos].group
            print "%s landed on %s (#%s)" % (player.name, property_name,
                                             player.pos)

            if propery_group == "Special":
                if property_name == "Chance":
                    if len(board.chance) == 0:
                        board.reset_chance()
                    # Get random card from deck
                    card = board.chance.pop(random.randrange(len(board.chance)))
                    print "Chance!"
                    print "'%s'" % card.description
                    # Execute action on card
                    card.func(board=board, player=player, players=players)
                elif property_name == "Income Tax":
                    tax = min(int(round(player.money*0.10)), 200)
                    player.money -= tax
                    board.free_parking += tax
                elif property_name == "Luxury Tax":
                    tax = 75
                    player.money -= tax
                    board.free_parking += tax

            # End of turn
            raw_input("Press Enter to continue... ")
            print "End of %s's turn\n" % player.name

        for player in players:
            print player

if __name__ == '__main__':
    run()
