from CheckerBoard import *


"""
currentPlayer starts at Player.black

movePiece:
    moves a piece IF the color matches the currentPlayer color and the move is valid

switchPlayer:
    changes the currentPlayer using currentPlayer = Player.other
"""



def takeTurn(board,currentPlayer):
    piece = None
    while piece == None:
        from_x = int(input("from x: "))
        from_y = int(input("from y: "))
        piece = board.getPieceAt(from_x, from_y)

        if piece == None:
            print("There is no piece there\n")

    to_x = int(input("to x: "))
    to_y = int(input("to y: "))

    # p = board.getPieceAt(from_x,from_y)
    assert piece is not None
    assert piece.color == currentPlayer
    moveIsJump = board.moveIsJump(piece, to_x, to_y)
    board.movePieceTo(piece,to_x,to_y)

    if moveIsJump and board.pieceCanJump(piece):
        takeDoubleJump(board, currentPlayer, piece)

def takeDoubleJump(board, currentPlayer, piece):
    doubleJumping = True
    while doubleJumping:
        # ask if they want to double jump
        answer = input("Would you like to double jump (y/n):\n")
        if answer != 'y':
            break
        # do the double jump
        try:
            to_x = int(input("\nto x:\n"))
            to_y = int(input("\nto y:\n"))

            assert(board.moveIsJump(piece, to_x, to_y))
        except:
            print("invalid double jump")
            continue

        board.movePieceTo(piece, to_x, to_y)
        if board.pieceCanJump(piece):
            takeDoubleJump(board, currentPlayer, piece)

def __main__():

    board = Board()

    print(board)

    currentPlayer = Player.black
    
    while True:
        
        try:
            takeTurn(board, currentPlayer)
        except:
            print("\nInvalid move. Try again.\n")
            continue
        print(board)
        currentPlayer = currentPlayer.other
        if currentPlayer == Player.black:
            print("Black's turn!")
        else:
            print("White's turn!")

__main__()
    

