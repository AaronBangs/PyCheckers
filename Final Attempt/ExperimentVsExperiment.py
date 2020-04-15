#JMJ
#AaronGame.py
#Plays a game of checkers between two AaronBots
#Programmed by Ben Campbell and Aaron Bangs

from CheckerGame import CheckerGame
#from Human import Human
#from RandomAI import RandomAI
from Loader import Loader
from AaronAI import AaronAI
from PyCheckers import Player
import random
import time

def __main__(num_of_games=0):
    game_num = 0

    time_list = []
    
    if num_of_games == 0:
        num_of_games = int(input('How many games would you like to simulate?\n'))

    test_start_time = time.time()
    while game_num < num_of_games:
        lowest = Loader.loadArray(0)[0]
        
        for x in range(1, 10):
            if Loader.loadArray(int(x))[0] < Loader.loadArray(int(x-1))[0]:
                lowest = x
        

        #lowest = random.randint(0,9)
        other = random.randint(0,9)
        if other == lowest:
            other = random.randint(0,9)
        
        blackPlayer = AaronAI(Player.black, lowest)
        whitePlayer = AaronAI(Player.white, other)

        game = CheckerGame(blackPlayer, whitePlayer, False)

        whiteLosses = whitePlayer.weightArray[0] #starts at 1 for the sake of confusion
        blackLosses = blackPlayer.weightArray[0]

        print("Game #%i: " % (game_num + 1), end='')

        start_time = time.time()
        playedGame = game.play(True)
        end_time = time.time()
        
        winner = "draw"
        
        if playedGame == Player.black:
            winner = "Player " + str(lowest)
        elif playedGame == Player.white:
            winner = "Player " + str(other)
        print("Winner: %s" % winner)
        length_time = end_time - start_time
        print("Time elapsed: %i seconds / %f minutes / %f hours\n" % (length_time, length_time/60, length_time/3600))
        
        if playedGame == Player.black:
            whitePlayer.tweak(1/(whiteLosses) + whiteLosses/blackLosses)
        elif playedGame == Player.white:
            blackPlayer.tweak(1/(blackLosses) + blackLosses/whiteLosses)
        else:
            blackPlayer.tweak(1/(blackLosses))
            whitePlayer.tweak(1/(whiteLosses))
        
        time_list.append(end_time - start_time)
        
        game_num += 1

    avg_time = avg(time_list)
    test_end_time = time.time()
    total_time = test_end_time - test_start_time
    print("Average time elapsed: %i seconds / %f minutes / %f hours" % (avg_time, avg_time/60, avg_time/3600))
    print("Total time: %i seconds / %f minutes / %f hours" % (total_time, total_time/60, total_time/3600))

def avg(l):
    t = 0
    for x in l:
        t += x
    return t / len(l)

__main__()
