from sympy import minimum
from handEvaluator import HandEvaluator
from player import *
from collections import Counter
import os

class Game():
    def __init__(self, playerNb) -> None:
        self.playerNb = playerNb
        self.players = []
        self.playersPot = [0]*3
        self.deck = Deck()
        self.deck.shuffle()
        self.flop = []
        for i in range(playerNb):
            self.players.append(Player(500000, str(i)))
        self.bigBlind = 0
        self.playersPot[self.bigBlind] += 10000
        self.players[self.bigBlind].setBalance(490000)
        self.smallBlind = 1
        self.players[self.smallBlind].setBalance(495000)
        self.playersPot[self.smallBlind] += 5000
        self.pot = 15000
        self.minimumBet = 10000
        self.you = self.players[2]
        self.currentMove = self.you
        os.system("CLS")
        print("===================== Game Start =====================")
        print("big blind : player " + str(self.bigBlind))
        print("small blind : player " + str(self.smallBlind))
        self.play()
        
    def showBoard(self):
        #show the current state of the board
        print("======================================================")
        print("Your cards are : " + str(self.you.getCards()[0]) + str(self.you.getCards()[1]))
        s = "Flop is : "
        for card in self.flop:
            s += str(card)
        print(s)
        print("pot is " + str(self.pot))
        print("minimum bet is " + str(self.minimumBet))
        print("your balance is " + str(self.you.getBalance()) + "$")
        print("======================================================")
    
    def isSomeoneTurn(self):
        #check if there is someone who still has to play
        check = False
        for i in range(self.playerNb):
            #TODO big blind can't raise first round
            if self.players[i].getIsPlaying() and (self.playersPot[i] < self.minimumBet or self.minimumBet == 0):
                check = True
        return check
    
    def hasEveryBodyChecked(self):
        #check if everybody has checked
        check = False
        for i in range(self.playerNb):
            if self.players[i].getIsPlaying() and self.players[i].getCheck() == False:
                check = True
        return check
    
    def turn(self):
        self.showBoard()
        #play a turn
        while self.isSomeoneTurn() and self.hasEveryBodyChecked():
            if self.currentMove.getIsPlaying():
                print("test")
                if self.currentMove == self.you:
                    self.playerMove()
                else:
                    self.botMove()
            currentIndex = int(self.currentMove.getIndex())
            if currentIndex == self.playerNb - 1:
                currentIndex = -1
            self.currentMove = self.players[currentIndex + 1]
            
        #reset players
        for p in self.players:
            p.setCanRaise(True)
            p.setCheck(False)
            self.playersPot[int(p.getIndex())] = 0
        self.minimumBet = 0
            
    def play(self):
        #give the cards
        for player in self.players:
            if player.getBalance() != 0:
                player.drawCard(self.deck.draw())
                player.drawCard(self.deck.draw())
        self.turn()
        
        #discard one card and put three on the flop
        self.deck.draw()
        self.flop.append(self.deck.draw())
        self.flop.append(self.deck.draw())
        self.flop.append(self.deck.draw())
        self.turn()
        for i in range(2):
            self.deck.draw()
            self.flop.append(self.deck.draw())
            self.turn()
        
        self.checkWinner()
                  
    def checkWinner(self):
        evaluator = HandEvaluator()
        i = 0
        while self.players[i].getIsPlaying() == False:
            i += 1
        winner = i
        winnerCombination = evaluator.checkBestCombination(self.flop, self.players[i].getCards())
        i += 1
        
        while i < self.playerNb:
            if self.players[i].getIsPlaying() == True:
                c2 = evaluator.checkBestCombination(self.flop, self.players[i].getCards())
                evaluation = evaluator.compareCombinations(winnerCombination, c2)
                if evaluation == 0:
                    pass
                elif evaluation[1] == 2:
                    winner = i
                    winnerCombination = evaluation[0]
            i += 1
        
        for player in self.players:
            if player.getIsPlaying():
                s = "player " + player.getIndex() + " has : "
                for card in player.getCards():
                    s += str(card)
                print(s)
        s = "Flop is : "
        for card in self.flop:
            s += str(card)
        print(s)
        s = "the winner is player " + str(winner) + " with "
        for card in winnerCombination[1]:
            s += str(card)
        print(s)
        self.players[winner].setBalance(self.players[winner].getBalance() + self.pot)
        x = input("press enter to continue")
        self.restart()
        
    def restart(self):
        self.bigBlind += 1
        if self.bigBlind == self.playerNb:
            self.bigBlind = 0
        self.playersPot[self.bigBlind] += 10000
        #TODO if balance < 10000 and if player isNotPlaying
        self.players[self.bigBlind].setBalance(self.players[self.bigBlind].getBalance() - 10000)
        self.smallBlind += 1
        if self.smallBlind == self.playerNb:
            self.smallBlind = 0
        self.playersPot[self.smallBlind] += 5000
        self.players[self.smallBlind].setBalance(self.players[self.smallBlind].getBalance() - 5000)
        self.pot = 15000
        self.minimumBet = 10000
        first = self.bigBlind + 1
        if first == self.playerNb:
            first = 0
        self.currentMove = self.players[first]
        os.system("CLS")
        print("===================== Game Start =====================")
        print("big blind : player " + str(self.bigBlind))
        print("small blind : player " + str(self.smallBlind))
        for p in self.players:
            if p.getBalance() > 0:
                p.setIsPlaying(True)
            else:
                p.setIsPlaying(False)
            p.setCards([])
        self.flop = []
        self.deck = Deck()
        self.deck.shuffle()
        self.play()
        
    def playerMove(self):
            if self.currentMove.getAllIn() == True:
                print("- player " + self.currentMove.getIndex() + " (you) : is ALL IN")
                self.currentMove.setCheck(True)
            else:
                move = int(input("player " + self.currentMove.getIndex() + " your turn : 1 to check; 2 to fold; 3 to raise; 4 to check the board "))
                if move == 1:
                    self.checkMove()
                elif move == 2:
                    self.foldMove() 
                elif move == 3:
                    self.raiseMove()
                #show the board
                elif move == 4:
                    self.showBoard()
                    self.playerMove()
                else:
                    print("wrong input")
                    self.playerMove()
                    
    def botMove(self):
        #for the moment only check and raise
        #TODO update it with ai
        index = self.currentMove.getIndex()
        if self.minimumBet == self.playersPot[int(index)]:
            print("- player " + index + " (bot) : check")
            self.currentMove.setCheck(True)
        elif self.minimumBet - self.playersPot[int(index)] < self.currentMove.getBalance():
            self.finalizeRaise(self.minimumBet - self.playersPot[int(index)],False,True)
        else:
            self.finalizeRaise(self.minimumBet - self.playersPot[int(index)],True,True)
                      
    def checkMove(self):
        #check
        if(self.minimumBet == 0 or self.playersPot[int(self.currentMove.getIndex())] == self.minimumBet):
            print("- player " + self.currentMove.getIndex() + " (you) : check")
            self.currentMove.setCheck(True)
        else:
            print("you cannot check!")
            self.playerMove()
    
    def foldMove(self):
        #fold
        if self.playersPot[int(self.currentMove.getIndex())] == self.minimumBet:
            print("your bet is the highest")
            self.playerMove()
        else:
            print("- player " + self.currentMove.getIndex() + " (you) : fold")  
            self.currentMove.setIsPlaying(False)
            
    def finalizeRaise(self, quantity, allIn, cpu = False):
        if allIn:
            if cpu:
                print("- player " + self.currentMove.getIndex() + " (bot) : is ALL IN " + str(quantity) + "$")
            else:
                print("- player " + self.currentMove.getIndex() + " (you) : is ALL IN " + str(quantity) + "$")
            #TODO set All in false
            self.currentMove.setAllIn(True)
            self.currentMove.setCheck(True)
        else:
            if cpu:
                print("- player " + self.currentMove.getIndex() + " (bot) : raised " + str(quantity) + "$")
            else:
                print("- player " + self.currentMove.getIndex() + " (you) : raised " + str(quantity) + "$")
        self.playersPot[int(self.currentMove.getIndex())] += quantity
        if self.playersPot[int(self.currentMove.getIndex())] > self.minimumBet:
            self.minimumBet = self.playersPot[int(self.currentMove.getIndex())]
        self.pot += quantity 
    
    def raiseMove(self):
        #raise
        quantity = int(input("quantity of money to raise "))           
        #raising the bet
        if quantity + self.playersPot[int(self.currentMove.getIndex())] > self.minimumBet and self.currentMove.getCanRaise():
            self.currentMove.setBalance(self.currentMove.getBalance() - quantity)
            if self.currentMove.getBalance() == 0:
                self.finalizeRaise(quantity, True)
            else:
                self.finalizeRaise(quantity, False)
            self.currentMove.setCanRaise(False) 
        #call
        elif quantity + self.playersPot[int(self.currentMove.getIndex())] == self.minimumBet:
            self.currentMove.setBalance(self.currentMove.getBalance() - quantity)
            if self.currentMove.getBalance() == 0:
                self.finalizeRaise(quantity, True)
            else:
                self.finalizeRaise(quantity, False)
        #raising to few
        else:
            print("impossible to complete the raise!")
            self.playerMove()            
                                      
def main():
    
    game = Game(3)
    
if __name__ == '__main__':
    main()