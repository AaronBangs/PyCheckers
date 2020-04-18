from RandomBot import RandomBot
import os
import time

class Controller:

  def __init__(self, blackBot, redBot):
    self.redBot = redBot
    self.blackBot = blackBot

  def runGame(self):

    while True:
        blackMove = self.blackBot.makemove()

        if blackMove == "resign":
            self.winner = self.redBot
            break

        self.redBot.receiveMove(blackMove)

        os.system("cls")
        print(self.blackBot.board)
        time.sleep(0.1)

        redMove = self.redBot.makemove()

        if redMove == "resign":
            self.winner = self.blackBot
            break

        self.blackBot.receiveMove(redMove)

        os.system("cls")
        print(self.blackBot.board)
        time.sleep(0.1)

    #print winner

def main():
    redBot = RandomBot("red", None)
    blackBot = RandomBot("black", None)
    controller = Controller(blackBot, redBot)
    controller.runGame()

if __name__ == "__main__":
    main()