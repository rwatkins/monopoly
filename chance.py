# Chance functions

import random

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