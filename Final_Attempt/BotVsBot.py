from AgentBots import RandomBot, MonteCarloBot
import os
import time

BLACK_BOT = MonteCarloBot("black")
RED_BOT = RandomBot("red")

'''
from PyCheckers import Board
s = """   0  1  2  3  4  5  6  7
0 ███   ███   ███   ███
1    ███   ███   ███   ███
2 ███ ○ ███   ███ ● ███
3    ███   ███   ███ ■ ███
4 ███ ○ ███ ○ ███ ○ ███
5    ███   ███   ███   ███
6 ███ □ ███   ███   ███
7    ███   ███   ███   ███"""
b = Board.from_string(s)
self.red_bot.board = b
self.black_bot.board = Board.from_string(str(b))


'''

class Controller:

    def __init__(self, black_bot, red_bot):
        self.red_bot = red_bot
        self.black_bot = black_bot
        self.winner = None

    def do_turn(self, mover, reciever):
        if self.winner != None:
            return
        
        move_is_valid = False

        while not move_is_valid:
            move = mover.make_move()

            if move == "resign":
                self.winner = reciever
                break

            move_is_valid = reciever.receive_move(move)
            if not move_is_valid:
                mover.undo_last_move()

        # os.system("cls")
        time.sleep(0.5)
        print(self.black_bot.get_board_str())

    def run_game(self):
        while self.winner == None:
            self.do_turn(self.red_bot, self.black_bot)
            self.do_turn(self.black_bot, self.red_bot)

        if self.winner == self.red_bot:
            print("Red wins!")
        else:
            print("Black wins!")

        input("Press a key to close")

def main():
    controller = Controller(BLACK_BOT, RED_BOT)
    controller.run_game()

if __name__ == "__main__":
    main()