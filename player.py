from collections import Counter
from itertools import combinations
import itertools
import random

class Card:
    def __init__(self, value, suit):
        self.__value = value
        self.__suit = suit
        
    def getValue(self) -> int:
        return self.__value
    
    def getSuit(self) -> str:
        return self.__suit
    
    def __str__(self) -> str:
        if self.__value == 1:
            value = "A"
        elif self.__value == 11:
            value =  "J"
        elif self.__value == 12:
            value =  "Q"
        elif self.__value == 13:
            value = "K"
        else :
            value = self.__value
        return str(value) + self.getSuit()+ " "

class Deck:
    def __init__(self) -> None:
        self.cards = []
        for suit in ["♠","♥","♦","♣"]:
            for value in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                self.cards.append(Card(value,suit))
    def shuffle(self) -> None:
        random.shuffle(self.cards)
    
    def getNumb(self) -> int:
        return self.cards.length
    
    def draw(self) -> Card:
        return self.cards.pop()
    
    def __str__(self) -> str:
        res = ""
        for card in self.cards:
            res += str(card)
        return res
    
class Player:
    def __init__(self, money, index):
        self.__balance = money
        self.__index = index
        self.__cards = []
        self.__isPlaying = True
        self.__canRaise = True
        self.__check = False
        self.__allIn = False
        
    def getIsPlaying(self) -> bool:
        return self.__isPlaying
    
    def setIsPlaying(self, isPlaying):
        self.__isPlaying = isPlaying
    
    def fold(self):
        self.setIsPlaying(False)
    
    def check(self):
        pass
    
    def getBalance(self) -> int:
        return self.__balance
    
    def setBalance(self, balance):
        self.__balance = balance
    
    def drawCard(self, card):
        self.__cards.append(card)
    
    def getCards(self):
        return self.__cards

    def getIndex(self):
        return self.__index
    
    def getCanRaise(self):
        return self.__canRaise
    
    def setCanRaise(self, canRaise):
        self.__canRaise = canRaise
        
    def getCheck(self):
        return self.__check
    
    def setCheck(self, check):
        self.__check = check

    def getAllIn(self):
        return self.__allIn
    
    def setAllIn(self, allIn):
        self.__allIn = allIn
        
   
class HandEvaluator:
    def evaluateHand(self, cards):
        def getVal(c : Card):
            return c.getValue()
        cards.sort(key = getVal)
        values = []
        suits = []
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
            return (7, cards)
        #full house
        if mostCommonRank[0][1] == 3 and mostCommonRank[1][1] == 2:
            return (6, cards)
        #flush
        if mostCommonSuit[0][1] == 5:
            return(5, cards)
        #straight
        if straight:
            return(4, cards)
        #three of a kind
        if mostCommonRank[0][1] == 3:
            return(3, cards)
        #double couple
        if mostCommonRank[0][1] == 2 and mostCommonRank[1][1] == 2:
            return(2, cards)
        #couple
        if mostCommonRank[0][1] == 2:
            return(1, cards)
        return(0, cards)
    def compareCombinations(self, c1, c2):
        if c1[0] == c2[0]:
            i = 4
            while c1[1][i].getValue() == c2[1][i].getValue() and i != -1:
                i -=1
            if i == -1 or c1[1][i].getValue() == c2[1][i].getValue():
                return 0
            elif c1[1][i].getValue() > c2[1][i].getValue():
                return c1
            else:
                return c2
        elif c1[0] > c2[0]:
            return c1
        else:
            return c2
            
    def checkBestCombination(self, flop, hand):
        cards = flop + hand
        combinations = itertools.combinations(cards, 5)
        bestHand = 0
        for c in combinations:
            if bestHand == 0:
                bestHand = self.evaluateHand(list(c))
            else:
                evaluation = self.evaluateHand(list(c))
                comp = self.compareCombinations(bestHand, evaluation)
                if comp != 0:
                    bestHand = comp
        return bestHand