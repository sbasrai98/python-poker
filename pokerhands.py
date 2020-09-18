def royalflush(total):
    lst = list(map(lambda x: (x._suit, x._rank), total))
    for suit in ['Diamonds', 'Hearts', 'Clubs', 'Spades']:
        if (suit, 10) in lst and (suit, 11) in lst and \
           (suit, 12) in lst and (suit, 13) in lst and \
           (suit, 14) in lst:
            return (10, 14)  # (HandRank, HighestValue)
    return False

def straightflush(total):
    lst = list(map(lambda x: (x._suit, x._rank), total))
    for suit in ['Diamonds', 'Hearts', 'Clubs', 'Spades']:
        for i in range(13, 5, -1):
            if (suit, i) in lst and (suit, i-1) in lst and \
                (suit, i-2) in lst and (suit, i-3) in lst and \
                (suit, i-4) in lst:
                return (9, i) # (HandRank, HighestValue)
        if (suit, 5) in lst and (suit, 4) in lst and \
            (suit, 3) in lst and (suit, 2) in lst and \
            (suit, 14) in lst:
            return (9, 5) # (HandRank, HighestValue)
    return False

def fourkind(total):
    lst = list(map(lambda x: x._rank, total))
    lst.sort()
    for i in range(len(total) - 3):   # assuming 7 so no multi's possible
        if lst[i] == lst[i+1] and lst[i] == lst[i+2] and \
           lst[i] == lst[i+3]:
           return (8, lst[i])  # (HandRank, HighestValue)
    return False

def threekind(total):
    lst = list(map(lambda x: x._rank, total))
    lst.sort()
    highest3 = False
    for i in range(len(total) - 2):
        if lst[i] == lst[i+1] and lst[i] == lst[i+2]:
            highest3 = lst[i]  # value of match
    if highest3:
        return (4, highest3) # (HandRank, HighestValue)
    return highest3 # highest3 is false

def pair(total):
    lst = list(map(lambda x: x._rank, total))
    lst.sort()
    highest2 = False
    for i in range(len(total) - 1):  
        if lst[i] == lst[i+1]:
            highest2 = lst[i]  # value of match
    if highest2:
        return (2, highest2) # (HandRank, HighestValue)
    return highest2 # highest2 is false

def fullhouse(total):
    if threekind(total) == False:
        return False
    else:
        rank3 = threekind(total)[1]
        remaining = []
        for c in total:
            if c._rank != rank3:
                remaining.append(c)
        
        if pair(remaining) == False:
            return False
        else:
            return (7, rank3, pair(remaining)[1]) 
            # (HandRank, Highest3kind, Highest2kind)

def flush(total):
    total.sort(key=lambda x: x._rank)
    high = False
    for c in total:
        suit = c._suit 
        count = 0
        for h in total:
            if h._suit == suit:
                count += 1
        if count > 4:
            high = c._rank 
    if high:
        return (6, high) # (HandRank, HighestValue)
    return high # high is false

def straight(total):
    lst = list(map(lambda x: (x._rank), total))
    if 10 in lst and 11 in lst and \
       12 in lst and 13 in lst and \
       14 in lst:
        return (5, 14)  # ace-high straight
    else:
        for i in range(13, 5, -1):
            if (i) in lst and (i-1) in lst and \
               (i-2) in lst and (i-3) in lst and \
               (i-4) in lst:
                return (5, i) # (HandRank, HighestValue)
        if 5 in lst and 4 in lst and \
           3 in lst and 2 in lst and \
           14 in lst:
            return (5, 5) # (HandRank, HighestValue)
    return False

def twopair(total):
    if pair(total) == False:
        return False
    else:
        rank2 = pair(total)[1]
        remaining = []
        for c in total:
            if c._rank != rank2:
                remaining.append(c)
        
        if pair(remaining) == False:
            return False
        else:
            return (3, rank2, pair(remaining)[1]) 
            # (HandRank, Highest2kind, Highest2kind)

def besthand(board, hand):
    total = board+hand
    checks = []
    checks.append(royalflush(total)) 
    checks.append(straightflush(total))
    checks.append(fourkind(total))
    checks.append(fullhouse(total)) 
    checks.append(flush(total)) 
    checks.append(straight(total)) 
    checks.append(threekind(total)) 
    checks.append(twopair(total))
    checks.append(pair(total))  
    for h in checks:
        if h:
            return h
    # otherwise, best hand is high card
    ranks = [hand[0]._rank, hand[1]._rank]
    return (1, max(ranks), min(ranks)) 

# store besthand() in var's p1 p2 p3 p4 etc.
# use compare function

def compare(hands): # list of hands
    
    handranks = list(map(lambda x: x[0], hands))
    toprank = max(handranks)
    besthands1 = list(filter(lambda x: x[0] == toprank, hands))
    if len(besthands1) == 1:
        return besthands1
    
    topval = max(list(map(lambda x: x[1], besthands1)))
    besthands2 = list(filter(lambda x: x[1] == topval, besthands1))
    #filtered through both vals
    if len(besthands2) == 1 or len(besthands2[0]) == 2: 
        return besthands2
    
    topval2 = max(list(map(lambda x: x[2], besthands1)))
    besthands3 = list(filter(lambda x: x[2] == topval2, besthands2))
    return besthands3

def readhand(hand): # tuple of codified hand
    hands = ["High Card", "Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", \
             "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"]
    return hands[hand[0]-1]

