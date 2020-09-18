import random
import time
from pokerhands import besthand, compare, readhand
from pokerprobability import betoption, raisebet


class Card:
    '''
    data type representing individual playing cards
    '''
    def __init__(self, suit, rank):
        self._suit = suit
        self._rank = rank

    def __repr__(self):
        if self._rank == 14:
            rnk = "Ace"
        elif self._rank == 11:
            rnk = "Jack"
        elif self._rank == 12:
            rnk = "Queen"
        elif self._rank == 13:
            rnk = "King"
        else:
            rnk = str(self._rank)
        return  rnk + " of " + self._suit

class CardDeck:
    '''
    data type representing a full deck of cards (52 cards, no jokers)
    '''
    def __init__(self):
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"]     
        ranks = list(range(2, 15))
        
        self._deck = []

        for suit in suits:
            for rank in ranks:
                self._deck.append(Card(suit, rank)) 
    
    def shuffle(self):
        '''
        randomly shuffles all cards in the deck
        '''
        shuffled = []
        while not(self._deck == []):
            cards = list(range(len(self._deck)))
            shuffled.append(self._deck.pop(random.choice(cards)))
        self._deck = shuffled

    def deal(self, players): 
        '''
        deals one card to each player in 'players'
        players: (listof (listof Card))
        '''
        for p in players:
            p.append(self._deck.pop(0))

class Poker:
    '''
    data type representing the full game, or a game state
    '''
    def __init__(self, players):
        self._deck = CardDeck()  # deck used for the game
        self._deck.shuffle()
        self._board = []         # community cards currently in play
        self._burnpile = []      # discard pile for used cards

        self._count = players
        self._player = []         # this is messy,
        self._playercash = []     # should use a Player object to simplify
        self._playerbets = []     #  implementation and consolidate player data
        self._folded = []         # ^^^

        self._order = list(range(players))   # order in which players bet (rotates)
        self._bet = 0                        # current wager
        self._pot = 0                        # current pot (pool of bets)
        for i in range(players):             # initialize player data
            self._player.append([])          # (use a Player object in next version)
            self._playercash.append(1000)
            self._playerbets.append(0)

    def __repr__(self):
        '''
        displays state of the game (current player balances, game board, etc.)
        '''
        game = "Your cards: "+str(self._player[0])+"\n"
        game += "Board: "+str(self._board)+"\n"

        for i in range(self._count):
            game += "P"+str(i+1)+": "+str(self._playercash[i])+" "    
        game += "\n" + "Pot: " + str(self._pot) + "\n"

        return game

    def show(self):
        '''
        displays all players' cards
        '''
        game = ""
        for i in range(self._count):
            game += "P"+str(i+1)+": "
            game += str(self._player[i])
            game += "\n" 
        print(game)

    def myturn(self):
        '''
        facilitates P1's (the user) turn to play
        '''
        if self._bet == 0:
            move = input("Check, Raise, or Fold? [ch/r/f]\n")
        else:
            move = input("Call, Raise, or Fold? [ca/r/f]\n")
        
        if move == "ch":
            print("P1: Check.")
            return
        if move == "ca":
            print("P1: Call.")
            putup = self._bet - self._playerbets[0]
            self._playercash[0] -= putup
            self._pot += putup
            self._playerbets[0] += putup
        if move == 'r':
            putup = self._bet - self._playerbets[0]
            self._playercash[0] -= putup
            self._pot += putup
            self._playerbets[0] += putup
            raising = input("How much?\n") ## will need fail safes for inputs.
            print("P1: Raise", raising)
            self._playercash[0] -= int(raising)
            self._bet += int(raising)
            self._pot += int(raising)
            self._playerbets[0] += int(raising)
        if move == 'f':
            print("P1: Fold.")
            self._folded.append(0)
            return
        
    def opturn(self, p):
        '''
        facilitates an opponent's (computer) turn to play
        p: an integer representing a player in the game
        '''
        move = betoption(self, p)

        if move == "ch":
            print("P"+str(p+1)+": Check.")
            return
        if move == "ca":
            print("P"+str(p+1)+": Call.")
            putup = self._bet - self._playerbets[p]
            self._playercash[p] -= putup
            self._pot += putup
            self._playerbets[p] += putup
        if move == 'r':
            putup = self._bet - self._playerbets[p]
            self._playercash[p] -= putup
            self._pot += putup
            self._playerbets[p] += putup
            raising = raisebet(self, p) 
            print("P"+str(p+1)+": Raise", raising)
            self._playercash[p] -= int(raising)
            self._bet += int(raising)
            self._pot += int(raising)
            self._playerbets[p] += int(raising)
        if move == 'f':
            print("P"+str(p+1)+": Fold.")
            self._folded.append(p)
            return

    def betround(self):
        '''
        processes a full betting round by allowing each player to play their turn
        '''
        for i in self._order:
            if not(i in self._folded):
                if i == 0:
                    self.myturn()
                else:
                    self.opturn(i)
                time.sleep(1)

        for i in self._order:  # players must decide whether to fold or call
            if not(i in self._folded) and self._playerbets[i] != self._bet:
                if i == 0:
                    move = input("Call or Fold? [ca/f]\n")
                    if move == "f":
                        print("P"+str(i+1)+": Fold.")
                        self._folded.append(i)
                    else:
                        print("P"+str(i+1)+": Call.")   
                        putup = self._bet - self._playerbets[i]
                        self._playercash[i] -= putup
                        self._pot += putup
                        self._playerbets[i] += putup
                else:
                    print("P"+str(i+1)+": Call.")   # opponents auto-call for now
                    putup = self._bet - self._playerbets[i]
                    self._playercash[i] -= putup
                    self._pot += putup
                    self._playerbets[i] += putup

        for i in range(self._count):                # reset betting variables
            self._playerbets[i] = 0
        self._bet = 0

    def cleanup(self):
        '''
        'cleans up' after a full round of the game has been played by resetting
          the state of the game, shuffling cards, rotating player order, etc.
        '''
        for i in range(self._count):
            self._burnpile.extend(self._player[i])
            self._player[i] = []
        self._burnpile.extend(self._board)
        self._board = []
        self._pot = 0
        self._folded = []
        if len(self._burnpile) > len(self._deck._deck):
            self._deck._deck.extend(self._burnpile)
            self._burnpile = []
            self._deck.shuffle()
        # rotate betting order
        self._order.append(self._order.pop(0))

    def checkfold(self):
        '''
        checks if only one player remains (all others have folded), in which
          case the remaining player wins by default
        '''
        if len(self._folded) == self._count - 1:
            for i in range(self._count):
                if not(i in self._folded):
                    print(self)
                    self.show()
                    print("P"+str(i+1)+" wins the pot by default.")
                    self._playercash[i] += self._pot
                    self.cleanup()
                    return True
        else:
            return False

    def play(self):
        '''
        processes a full round of poker 
          (betting, dealing cards, alotting winnings, etc.)
        '''
        print("All players: Ante 10")   # ante from all players
        for i in range(self._count):
            self._playercash[i] -= 10
            self._pot += 10
        time.sleep(1)

        self._deck.deal(self._player)   # deal cards to players
        self._deck.deal(self._player)
        print(self)
        
        print("*first betting round*")
        self.betround()
        if self.checkfold():
            return

        time.sleep(1)
        self._deck.deal([self._board])  # deal "the flop" (first 3 community cards)
        self._deck.deal([self._board]) 
        self._deck.deal([self._board])
        print(self)

        print("*second betting round*")
        self.betround()
        if self.checkfold():
            return

        time.sleep(1)
        self._deck.deal([self._board])  # deal "the turn" (4th community card)
        print(self)
        print("*third betting round*")
        self.betround()
        if self.checkfold():
            return

        time.sleep(1)
        self._deck.deal([self._board])  # deal "the river" (5th community card)
        print(self)
        print("*fourth betting round*")
        self.betround()
        if self.checkfold():
            return

        time.sleep(1)
        print(self)
        print("Show cards.")
        self.show()

        # give winner winnings, print who won, what hand
        time.sleep(1)
        hands = []
        for h in self._player:  
            hands.append(besthand(self._board, h))
        for i in self._folded:
            hands[i] = (0, 0)   # make folded players ineligible
        wins = compare(hands)
        winners = []
        for i in range(self._count):
            if hands[i] in wins:
                winners.append(i)
        if len(winners) == 1:   # one players wins
            print('P'+str(winners[0]+1)+' wins the pot with a '+readhand(wins[0])+'.')
            self._playercash[winners[0]] += self._pot
        else:                   # tie between multiple players
            wnrs = '('
            for w in winners:
                wnrs += str(w+1)
            wnrs += ')'
            print("Tie between P"+wnrs+'.')
            share = self._pot // len(winners)
            for w in winners:
                self._playercash[w] += share
        self.cleanup()

    def loop(self):
        '''
        play loop allowing for repeated rounds of play until the user quits
        '''
        while True:
            self.play()
            cont = input("Continue or Quit? [c/q]\n")
            if cont == 'q':
                break
        print("Final Totals:")
        game = ""
        for i in range(self._count):
            game += "P"+str(i+1)+": "+str(self._playercash[i])+" "
        print(game+'\n') 

# to play the game
p = Poker(4)  # create a Poker object (for 4 players, in this case)
p.loop()      # begin the play loop
