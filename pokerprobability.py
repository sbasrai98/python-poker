from pokerhands import besthand
import random


def raisebet(game, p):
    '''
    produces the value player p will raise the bet by
    '''
    hand = besthand(game._board, game._player[p])

    # bet limits: min = 10, max = 200
    if hand[0] <= 2:
        return str(random.randint(10, 50))
    if hand[0] <= 5:
        return str(random.randint(30, 100))
    if hand[0] <= 7:
        return str(random.randint(70, 150))
    else:
        return str(random.randint(110, 200))

def betoption(game, p):
    '''
    produces a string corresponding to player p's move
    '''
    hand = besthand(game._board, game._player[p])
    # how strong is the hand?
    if hand[0] >= 8:
        strength = 3
    elif hand[0] >= 4:
        strength = 2
    elif hand[0] >= 2:
        strength = 1
    else:
        strength = 0

    # what is the current betting round? used as multiplicative factor
    if len(game._board) == 0:
        round = 1
    if len(game._board) == 3:
        round = 2
    if len(game._board) == 4:
        round = 3
    if len(game._board) == 5:
        round = 4

    # what fraction of the player's balance is the current bet?
    betfrac = game._bet / (game._playercash[p] + game._playerbets[p])

    # fold if betfrac > foldround[round-1][strength]
    foldround = ( [0.1, 1, 1, 1], [0.2, 0.3, 0.4, 1], \
                  [0.3, 0.4, 0.5, 1], [0.4, 0.5, 0.6, 1] )

    if betfrac > foldround[round-1][strength]:
        return 'f'

    # if not folding, either raising or 'stay'ing
    if game._bet == 0:
        stay = 'ch'
    else:
        stay = 'ca'

    # pfactor cutoffs for "raise/call" options. 
    # if pfactor < raiseround[round-1][strength]

    raiseround = ( [0.2, 0.6, 0.6, 0.6], [0.1, 0.5, 0.7, 0.9], \
                   [0.08, 0.3, 0.6, 0.8], [0.03, 0.1, 0.6, 0.7] )

    pfactor = random.random()
    if pfactor < raiseround[round-1][strength]:
        return 'r'
    else:
        return stay
