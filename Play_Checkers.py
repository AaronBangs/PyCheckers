from CheckerBoard import *


"""
currentPlayer starts at Player.black

movePiece:
    moves a piece IF the color matches the currentPlayer color and the move is valid

switchPlayer:
    changes the currentPlayer using currentPlayer = Player.other
"""



def takeTurn(board,currentPlayer,from_x,from_y,to_x,to_y):
    p = board.getPieceAt(from_x,from_y)
    assert p is not None
    assert p.color == currentPlayer
    board.movePieceTo(p,to_x,to_y)

def __main__():

    board = Board()

    print(board)

    currentPlayer = Player.black
    
    while True:
        fx = int(input("\nfrom x:\n"))
        fy = int(input("\nfrom y:\n"))
        tx = int(input("\nto x:\n"))
        ty = int(input("\nto y:\n"))
        try:
            takeTurn(board, currentPlayer, fx, fy, tx, ty)
        except:
            print("\nInvalid move. Try again.\n")
            continue
        print(board)
        currentPlayer = currentPlayer.other

__main__()
    

