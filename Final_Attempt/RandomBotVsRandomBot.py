from RandomBot import RandomBot
import os
import time

class Controller:

    def __init__(self, blackBot, redBot):
        self.redBot = redBot
        self.blackBot = blackBot

    def do_turn(self, mover, reciever):
        move_is_valid = False

        while not move_is_valid:
            move = mover.makemove()

            if move == "resign":
                self.winner = reciever
                break

            move_is_valid = reciever.receiveMove(move)
            if not move_is_valid:
                mover.undo_last_move()

        os.system("cls")
        print(self.blackBot.board)
        time.sleep(0.1)

    def runGame(self):
        while True:
            self.do_turn(self.redBot, self.blackBot)
            self.do_turn(self.blackBot, self.redBot)

    #print winner

def main():
    redBot = RandomBot("red", None)
    blackBot = RandomBot("black", None)
    controller = Controller(blackBot, redBot)
    controller.runGame()

if __name__ == "__main__":
    main()