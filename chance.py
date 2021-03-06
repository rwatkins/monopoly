class Chance(object):
    """A card from the Chance deck."""
    def __init__(self, description, func):
        self.description = description
        self.func = func

# Chance functions
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
    player.status = "In Jail"
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
    board.free_parking += cost
    return

def pay_poor_tax(**kwargs):
    """Pay poor tax of $15"""
    assert "board" in kwargs.keys(), "'board' not found in arguments"
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player, board = kwargs["player"], kwargs["board"]
    player.money -= 15
    board.free_parking += 15
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
        if p.status != "Out":
            player.money -= 50
            p.money += 50
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

def advance_to_st_charles_place(**kwargs):
    """(Chance card text here)"""
    assert "player" in kwargs.keys(), "'player' not found in arguments"
    player = kwargs["player"]
    player.move_to(11)
    return

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
#def get_out_of_jail_free_card(**kwargs):
#    player.has_get_out_of_jail_free_card = True
#    return

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
    ),
    Chance(
        "(Chance card text here)",
        advance_to_st_charles_place
    )
]
