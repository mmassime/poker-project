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
        self.preFlop()
        
    def board(self):
        print("Your cards are : " + str(self.you.getCards()[0]) + str(self.you.getCards()[1]))
        print("pot is " + str(self.pot))
        print("minimum bet is " + str(self.minimumBet))
    
    def isSomeoneTurn(self):
        check = False
        for i in range(self.playerNb):
            if self.players[i].getIsPlaying and self.playersPot[i] < self.minimumBet:
                check = True
        return check
    
    def turn(self):
        while self.isSomeoneTurn():
            if self.currentMove.getIsPlaying and self.playersPot[int(self.currentMove.getIndex())] < self.minimumBet:
                if self.currentMove == self.you:
                    self.playerMove()
                else:
                    #bot for now can only check or call
                    currentPlayerPot = self.playersPot[int(self.currentMove.getIndex())]
                    if currentPlayerPot < self.minimumBet:
                        self.currentMove.setBalance(self.currentMove.getBalance() - self.minimumBet-currentPlayerPot)
                        print("- player " + self.currentMove.getIndex() + " : raised " + str(self.minimumBet-currentPlayerPot) + "$")
                        currentPlayerPot = self.minimumBet
                        
                    else:
                        print("- player " + self.currentMove.getIndex() + " : check")
            currentIndex = int(self.currentMove.getIndex())
            if currentIndex == self.playerNb - 1:
                currentIndex = -1
            self.currentMove = self.players[currentIndex + 1]
    def preFlop(self):
        for player in self.players:
            player.drawCard(self.deck.draw())
            player.drawCard(self.deck.draw())
        self.board()
        self.turn()
          
    def playerMove(self):
            move = int(input("your turn : 1 to check; 2 to fold; 3 to raise; 4 to check the board "))
            if move == 1:
                if(self.minimumBet == 0):
                    print("- player " + self.currentMove.getIndex() + " (you) : check")
                else:
                    print("you cannot check!")
                    self.playerMove()
            if move == 2:
                print("- player " + self.currentMove.getIndex() + " (you) : fold")  
                self.currentMove.setIsPlaying(False) 
            if move == 3:
                quantity = int(input("quantity of money to raise "))
                if quantity + self.playersPot[int(self.currentMove.getIndex())] > self.minimumBet and self.currentMove.getCanRaise():
                    self.currentMove.setBalance(self.currentMove.getBalance() - quantity)
                    print("- player " + self.currentMove.getIndex() + " (you) : raised " + str(quantity) + "$")
                    self.playersPot[int(self.currentMove.getIndex())] += quantity
                    self.currentMove.setCanRaise(False)
                    self.minimumBet = self.playersPot[int(self.currentMove.getIndex())]
                elif quantity + self.playersPot[int(self.currentMove.getIndex())] == self.minimumBet:
                    self.currentMove.setBalance(self.currentMove.getBalance() - quantity)
                    print("- player " + self.currentMove.getIndex() + " (you) : raised " + str(quantity) + "$")
                    self.playersPot[int(self.currentMove.getIndex())] += quantity
                else:
                    print("you have to raise more!")
                    self.playerMove()
            if move == 4:
                self.board()
                
                    
                
            
            
def main():
    
    deck = Deck()
    deck.shuffle()
    
    gmae = Game(3)
    
if __name__ == '__main__':
    main()