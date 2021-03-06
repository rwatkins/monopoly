import copy
import random
from chance import *

class Property(object):
    """A single square on the game board."""
    def __init__(self, name, group, price=0, mandatory=False):
        self.name = name
        self.group = group
        self.price = price
        self.mandatory = mandatory
        self.is_purchasable = self.group != "Special" and self.group != "Tax"
        self.owner = None # this will be a Player object
        self.hotel = 0
        self.houses = 0

    def __repr__(self):
        return "<%s(name='%s', group='%s', price=%s)>" % \
            (self.__class__.__name__, self.name, self.group, self.price)

class Board(object):
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

        # group_count is a dict containing the number of properties in each
        # color group. It is used to determine if a player owns all properties
        # of a particular color group.
        self.group_count = self.get_group_count()

        # Chance cards
        self.chance = copy.deepcopy(DEFAULT_CHANCE_DECK)

        # Community Chest cards
        self.community_chest = []

        self.free_parking = 0

    def reset_chance(self):
        self.chance = copy.deepcopy(DEFAULT_CHANCE_DECK)

    def get_group_count(self):
        group_count = {}
        p_sorted = sorted([p.group for p in self.properties])
        for p in p_sorted:
            if p in group_count.keys():
                group_count[p] += 1
            else:
                group_count[p] = 1
        return group_count

class Player(object):
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

    def owns_group(self, color_group, group_count):
        """
        Returns True if the player owns all properties in the given color
        group. Property counts must be set in the group_count dict argument.
        """
        count = 0
        for p in self.properties:
            if p.group == color_group:
                count += 1
        return count == group_count[color_group]

    def num_properties_owned(self, color_group=""):
        """
        Returns the number of properties owned that belong to the specified
        color group. If no color group is given, return number of total
        properties owned.
        """
        if color_group == "":
            return len(self.properties)
        else:
            return len([p for p in self.properties if p.group == color_group])

def roll_dice(num_of_dice=1):
    """
    Returns a list of length num_of_dice, with each element containing the
    number that was rolled on that die.
    """
    sides = 6
    return [random.randrange(1, sides+1) for _ in xrange(num_of_dice)]

def run():
    board = Board()
    players = []
    players.append(Player("Riley"))
    players.append(Player("Scott"))
    players.append(Player("Elizabeth"))
    players.append(Player("Rosalie"))
    current_round = 0
    players_in_play = len(players)
    game_over = False

    print "Welcome to Monopoly!"
    print "Starting new game..."

    while True:
        # End the game at round 10000
        if current_round >= 10000:
            game_over = True
            print "\nReached", current_round, "rounds. Game over."
            break
        current_round += 1
        print "\n\n###### Round", current_round, "######\n"

        for player in players:
            if game_over == True:
                break

            if player.status == "Out":
                print "## Skip %s's turn, player out of money ##\n" % player.name
                continue

            print "%s's turn" % player.name

            # Player rolls dice
            dice = roll_dice(2)
            print "%s rolled %s" % (player.name, dice)

            # Move number of spaces on dice
            player.move_to(player.pos+sum(dice))
            prop = board.properties[player.pos]
            print "%s landed on %s (#%s)" % (player.name, prop.name,
                                             player.pos)

            if prop.group == "Special":
                if prop.name == "Chance":
                    if len(board.chance) == 0:
                        board.reset_chance()
                    # Get random card from deck
                    card = board.chance.pop(random.randrange(len(board.chance)))
                    print "Chance!"
                    print "'%s'" % card.description
                    # Execute action on card
                    card.func(board=board, player=player, players=players)
                elif prop.name == "Income Tax":
                    tax = min(int(round(player.money*0.10)), 200)
                    player.money -= tax
                    board.free_parking += tax
                elif prop.name == "Luxury Tax":
                    tax = 75
                    player.money -= tax
                    board.free_parking += tax
                elif prop.name == "Free Parking":
                    if board.free_parking > 0:
                        print "Free Parking! %s earns $%s" % \
                            (player.name, board.free_parking)
                        player.money += board.free_parking
                        board.free_parking = 0
                    else:
                        print "Free Parking is empty :("
            elif prop.group == "Railroad":
                if prop.owner is None:
                    if buy_prop(player, prop):
                        print "%s buys %s for $%s" % (player.name, prop.name,
                                                      prop.price)
                    else:
                        print "%s is unable to buy %s" % (player.name,
                                                          prop.name)
                elif player is not prop.owner:
                    rent_scale = (None, 25, 50, 100, 200)
                    rent = rent_scale[prop.owner.num_properties_owned(prop.group)]
                    print "%s owns %s, %s pays $%s rent." % (prop.owner.name,
                                                             prop.name,
                                                             player.name,
                                                             str(rent))
                    rent = rent if player.money >= rent else player.money
                    player.money -= rent
                    prop.owner.money += rent
                else:
                    print "%s already owns %s." % (player.name, prop.name)
            elif prop.group == "Utility":
                pass
            else:
                if prop.owner is None:
                    if buy_prop(player, prop):
                        print "%s buys %s for $%s" % (player.name, prop.name,
                                                      prop.price)
                    else:
                        print "%s is unable to buy %s" % (player.name,
                                                          prop.name)
                else:
                    rent = int(prop.price + prop.price * prop.hotel)
                    print "%s owns %s, %s pays $%s rent." % (prop.owner.name,
                                                             prop.name,
                                                             player.name,
                                                             str(rent))
                    rent = rent if player.money >= rent else player.money
                    player.money -= rent
                    prop.owner.money += rent

            if player.money <= 0:
                print "%s ran out of money! %s is out of the game.\n" % \
                    (player.name, player.name)
                player.status = "Out"
                for prop in board.properties:
                    if prop.owner is not None and prop.owner.name == player.name:
                        prop.owner = None
                player.properties = []
                players_in_play -= 1
                if players_in_play == 1:
                    game_over = True
                    break
            else:
                # Buy hotels
                for p in player.properties:
                    if p.hotel:
                        continue
                    hotel_price = p.price * 4
                    if board.available_hotels and player.money > hotel_price and\
                        player.owns_group(p.group, board.group_count):
                        print "%s buys a hotel on %s for %s\n" % (player.name,
                                                                  prop.name,
                                                                  hotel_price)
                        player.money -= hotel_price
                        p.hotel = 1
                        board.available_hotels -= 1

            print "End of %s's turn\n" % player.name

        for player in players:
            print player

        if game_over == True:
            break

        #raw_input("End of round. Press Enter to continue... ")

    for player in players:
        if player.status != "Out":
            winner = player
            for p in players:
                if winner.money < p.money:
                    winner = p
    print "\n%s wins !" % winner.name
    print "\nHotels left: %s" % board.available_hotels
    return

def buy_prop(player, prop):
    """Returns True if the purchase was successful."""
    if player.money >= prop.price:
        player.money -= prop.price
        prop.owner = player
        player.properties.append(prop)
        return True
    else:
        return False

if __name__ == '__main__':
    run()
