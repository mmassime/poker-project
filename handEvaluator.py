from collections import Counter
import itertools
from player import Card

class HandEvaluator:
    def evaluateCards(self, cards):
        #take 5 cards and return a tuple (a score of the cards, the cards in increasing order, higher card of the combination)
        def getVal(c : Card):
            #used to sort the cards
            return c.getValue()
        cards.sort(key = getVal)
        values = []
        suits = []
        #separate suits and ranks
        for card in cards:
            values.append(card.getValue())
            suits.append(card.getSuit())
        straight = False
        if values[4] == values[3] + 1 and values[3] == values[2] + 1 and values[2] == values[1] + 1 and (values[1] == values[0] + 1 or values[4] == values[0] + 12):
            straight = True 
        #check for 5 same suits
        counterSuits = Counter(suits)
        counterRanks = Counter(values)
        mostCommonSuit = counterSuits.most_common()
        mostCommonRank = counterRanks.most_common(2)
        if mostCommonSuit[0][1] == 5:
            if straight:
                #royal flush
                if values[0] == 1 and values[4] == 13:
                    return(9, cards)
                #straight flush
                else:
                    return(8, cards)
            pass
        #four of a kind
        if mostCommonRank[0][1] == 4:
            return (7, cards, mostCommonRank[0][0])
        #full house
        if mostCommonRank[0][1] == 3 and mostCommonRank[1][1] == 2:
            return (6, cards, mostCommonRank[0][0], mostCommonRank[1][0])
        #flush
        if mostCommonSuit[0][1] == 5:
            return(5, cards)
        #straight
        if straight:
            return(4, cards)
        #three of a kind
        if mostCommonRank[0][1] == 3:
            return(3, cards, mostCommonRank[0][0])
        #double couple
        if mostCommonRank[0][1] == 2 and mostCommonRank[1][1] == 2:
            return(2, cards, mostCommonRank[1][0], mostCommonRank[0][0])
        #couple
        if mostCommonRank[0][1] == 2:
            return(1, cards, mostCommonRank[0][0])
        return(0, cards)
    
    def compareCombinations(self, c1, c2):
        if c1[0] == c2[0]:
            #if it's a couple, three of a kind or poker win the bigger rank
            if c1[0] == 1 or c1[0] == 3 or c1[0] == 7:
                if c1[2] > c2[2]:
                    return (c1,1)
                elif c1[2] < c2[2]:
                    return (c2, 2)
            #if it's a full or a double couple check both the ranks
            if c1[0] == 2 or c1[0] == 6:
                if c1[2] > c2[2]:
                    return (c1,1)
                elif c1[2] < c2[2]:
                    return (c2, 2)
                elif c1[3] > c2[3]:
                    return (c1,1)
                elif c1[3] < c2[3]:
                    return (c2, 2)
            #otherwise win the highest cards
            i = 4
            while c1[1][i].getValue() == c2[1][i].getValue() and i != -1:
                i -=1
            if i == -1 or c1[1][i].getValue() == c2[1][i].getValue():
                return 0
            elif c1[1][i].getValue() > c2[1][i].getValue():
                return (c1,1)
            else:
                return (c2, 2)
        elif c1[0] > c2[0]:
            return (c1,1)
        else:
            return (c2, 2)
            
    def checkBestCombination(self, flop, hand):
        #check all the combination of 5 cards between the 7 possible and return the best
        cards = flop + hand
        combinations = itertools.combinations(cards, 5)
        bestHand = 0
        for c in combinations:
            if bestHand == 0:
                bestHand = self.evaluateCards(list(c))
            else:
                evaluation = self.evaluateCards(list(c))
                comp = self.compareCombinations(bestHand, evaluation)
                if comp != 0:
                    bestHand = comp[0]
        return bestHand