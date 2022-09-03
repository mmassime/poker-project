from player import *

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
        self.bigBlind = self.players[0]
        self.playersPot[0] += 10000
        self.bigBlind.setBalance(490000)
        self.smallBlind = self.players[1]
        self.smallBlind.setBalance(495000)
        self.playersPot[1] += 5000
        self.pot = 15000
        self.minimumBet = 10000
        self.you = self.players[2]
        self.currentMove = self.you
        print("===================== Game Start =====================")
        print("big blind : player " + self.bigBlind.getIndex())
        print("small blind : player " + self.smallBlind.getIndex())
        self.play()
        
    def showBoard(self):
        #show the current state of the board
        print("Your cards are : " + str(self.you.getCards()[0]) + str(self.you.getCards()[1]))
        s = "Flop is : "
        for card in self.flop:
            s += str(card)
        print(s)
        print("pot is " + str(self.pot))
        print("minimum bet is " + str(self.minimumBet))
    
    def isSomeoneTurn(self):
        #check if there is someone who still has to play
        check = False
        for i in range(self.playerNb):
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
                self.playerMove()
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
        pass
            
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
                
    def checkMove(self):
        #check
        if(self.minimumBet == 0 or self.playersPot[int(self.currentMove.getIndex())] == self.minimumBet):
            print("- player " + self.currentMove.getIndex() + " (you) : check")
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
            
    def finalizeRaise(self, quantity, allIn):
        if allIn:
            print("- player " + self.currentMove.getIndex() + " (you) : is ALL IN " + str(quantity) + "$")
            #TODO set All in false
            self.currentMove.setAllIn(True)
            self.currentMove.setCheck(True)
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
    
    deck = Deck()
    deck.shuffle()
    
    game = Game(3)
    
if __name__ == '__main__':
    main()