import random

class Card:
    def __init__(self, value, suit):
        self.__value = value
        self.__suit = suit
        
    def getValue(self) -> str:
        return self.__value
    
    def getSuit(self) -> str:
        return self.__suit
    
    def __str__(self) -> str:
        return self.getValue() + " " + self.getSuit()+ " "

class Deck:
    def __init__(self) -> None:
        self.cards = []
        for suit in ["♠","♥","♦","♣"]:
            for value in ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
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